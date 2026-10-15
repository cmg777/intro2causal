#!/usr/bin/env python3
"""Export audited PNG/WebP masters, bundle evidence, and clean explicit run drafts."""

import argparse
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path

from PIL import Image


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_new_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as f:
        json.dump(value, f, indent=2)
        f.write("\n")


def check_audit(path, image_hash):
    audit = read_json(path)
    if audit.get("status") != "passed" or audit.get("image_reviewed") is not True:
        raise ValueError("A passed audit of the actual image is required")
    if audit.get("source_sha256") != image_hash:
        raise ValueError("Audit hash does not match the reviewed PNG")
    required = {"content", "numbers", "geometry", "presentation"}
    seen = set()
    for row in audit.get("checks", []):
        if row.get("status") not in {"pass", "not_applicable"}:
            raise ValueError("Audit contains a failed or unresolved check")
        if not isinstance(row.get("evidence"), str) or not row["evidence"].strip():
            raise ValueError("Every audit check needs evidence or an applicability reason")
        seen.add(row.get("category"))
    if not required <= seen:
        raise ValueError("Audit must cover content, numbers, geometry and presentation")
    # There is always content and a presentation to inspect, even for nonnumeric maps.
    for category in ("content", "presentation"):
        if not any(r.get("category") == category and r.get("status") == "pass"
                   for r in audit["checks"]):
            raise ValueError(f"{category} cannot be not_applicable")
    return audit


def check_pixels(png, webp):
    with Image.open(png) as a, Image.open(webp) as b:
        if a.format != "PNG" or b.format != "WEBP" or a.size != b.size:
            raise ValueError("Invalid formats or changed dimensions")
        if a.convert("RGBA").tobytes() != b.convert("RGBA").tobytes():
            raise ValueError("WebP is not pixel-identical to the PNG")
        return list(a.size)


def checked_export(path):
    manifest = read_json(path)
    if manifest.get("export_validated") is not True:
        raise ValueError("Export is not validated")
    png, webp = Path(manifest["png"]), Path(manifest["webp"])
    if digest(png) != manifest["png_sha256"] or digest(webp) != manifest["webp_sha256"]:
        raise ValueError("Export file changed since verification")
    check_audit(manifest["audit"], digest(png))
    check_pixels(png, webp)
    return manifest


def export(args):
    source, audit = Path(args.source).resolve(), Path(args.audit).resolve()
    output, manifest_path = Path(args.output_dir).resolve(), Path(args.manifest).resolve()
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", args.stem):
        raise ValueError("Use a lowercase hyphenated output stem")
    if manifest_path.exists():
        raise ValueError("Manifest already exists; use a new run path")
    source_hash = digest(source)
    check_audit(audit, source_hash)
    with Image.open(source) as img:
        if img.format != "PNG":
            raise ValueError("The selected master must be a PNG")
        img.load()
        output.mkdir(parents=True, exist_ok=True)
        pattern = re.compile(re.escape(args.stem) + r"-v(\d+)\.(?:png|webp)$")
        versions = [int(m.group(1)) for p in output.iterdir()
                    if (m := pattern.fullmatch(p.name))]
        version = max(versions, default=0) + 1
        png = output / f"{args.stem}-v{version}.png"
        webp = output / f"{args.stem}-v{version}.webp"
        created = []
        try:
            # Exclusive file creation; no accepted master is overwritten.
            with png.open("xb") as f:
                created.append(png)
                f.write(source.read_bytes())
            with webp.open("xb") as f:
                created.append(webp)
                img.convert("RGBA").save(f, format="WEBP", lossless=True, exact=True, method=6,
                                         icc_profile=img.info.get("icc_profile", b""),
                                         exif=img.info.get("exif", b""))
            size = check_pixels(png, webp)
            if digest(png) != source_hash:
                raise ValueError("PNG changed during export")
            manifest = {"source": str(source), "audit": str(audit), "stem": args.stem,
                        "version": version, "png": str(png), "webp": str(webp),
                        "png_sha256": digest(png), "webp_sha256": digest(webp),
                        "dimensions": size, "export_validated": True}
            write_new_json(manifest_path, manifest)
        except Exception:
            for p in created:
                p.unlink(missing_ok=True)
            raise
    return manifest


def bundle(args):
    files = set()
    for path in args.manifests:
        manifest = checked_export(path)
        files.update([Path(path).resolve(), Path(manifest["png"]),
                      Path(manifest["webp"]), Path(manifest["audit"])])
    files.update(Path(p).resolve() for p in args.include)
    entries, used = [], set()
    for p in sorted(files):
        if not p.is_file():
            raise ValueError(f"Missing bundle file: {p}")
        try:
            name = p.relative_to(Path.cwd().resolve()).as_posix()
        except ValueError:
            name = p.name
        if name in used:
            raise ValueError(f"Archive name collision: {name}")
        used.add(name)
        entries.append((p, name))
    output = Path(args.output)
    if output.resolve() in files:
        raise ValueError("Archive cannot include itself")
    output.parent.mkdir(parents=True, exist_ok=True)
    created = False
    try:
        with zipfile.ZipFile(output, "x", compression=zipfile.ZIP_DEFLATED) as z:
            created = True
            for p, name in entries:
                z.write(p, name)
        with zipfile.ZipFile(output) as z:
            if z.testzip() is not None or len(z.namelist()) != len(entries):
                raise ValueError("Archive verification failed")
    except Exception:
        if created:
            output.unlink(missing_ok=True)
        raise
    return {"archive": str(output.resolve()), "files": len(entries), "verified": True}


def cleanup(args):
    manifest = checked_export(args.manifest)
    root = Path(args.draft_root).resolve()
    source = Path(manifest["source"])
    if not root.is_dir() or root.name != "drafts":
        raise ValueError("Expected an existing run-specific drafts directory")
    if Path(args.manifest).resolve().parent != root.parent:
        raise ValueError("Export manifest must belong to the same run as drafts")
    if not source.is_relative_to(root):
        raise ValueError("Draft root does not contain this export's source")
    protected = {Path(manifest[k]).resolve() for k in ("png", "webp", "audit")}
    protected.add(Path(args.manifest).resolve())
    paths = []
    # Preflight the entire set BEFORE deleting anything.
    for arg in args.files:
        raw = Path(arg)
        p = raw.resolve()
        if raw.is_symlink() or not p.is_relative_to(root) or p in protected:
            raise ValueError(f"Not an unprotected draft within this run: {arg}")
        if p.suffix.lower() not in {".png", ".webp", ".jpg", ".jpeg", ".avif"}:
            raise ValueError(f"Refusing to delete evidence/non-image file: {arg}")
        if not p.is_file():
            raise ValueError(f"Draft does not exist: {arg}")
        if p not in paths:
            paths.append(p)
    for p in paths:
        p.unlink()
    return {"deleted": [str(p) for p in paths], "accepted_png": manifest["png"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("export")
    for name in ("source", "audit", "output-dir", "stem", "manifest"):
        p.add_argument("--" + name, required=True)
    p.set_defaults(func=export)
    p = sub.add_parser("bundle")
    p.add_argument("--manifests", nargs="+", required=True)
    p.add_argument("--include", nargs="*", default=[])
    p.add_argument("--output", required=True)
    p.set_defaults(func=bundle)
    p = sub.add_parser("cleanup")
    p.add_argument("--manifest", required=True)
    p.add_argument("--draft-root", required=True)
    p.add_argument("--files", nargs="+", required=True)
    p.set_defaults(func=cleanup)
    args = parser.parse_args()
    try:
        print(json.dumps(args.func(args), indent=2))
    except (ValueError, KeyError, OSError, json.JSONDecodeError) as e:
        parser.exit(1, f"Error: {e}\n")


if __name__ == "__main__":
    main()
