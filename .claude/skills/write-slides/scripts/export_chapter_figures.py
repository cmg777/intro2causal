#!/usr/bin/env python3
"""export_chapter_figures.py — stage a chapter's rendered figures for a slide deck.

intro2causal chapter plots are produced by executed matplotlib at Quarto render time —
there are no pre-saved PNGs with stable names. This helper collects the figures the
book render already emits to `book/_book/notebooks_quarto/<base>_files/figure-html/*.png`,
maps each to the section heading it appears under, and copies them (plus the chapter's
visual-summary image) into the deck's `_figcache/` staging dir with ordered, meaningful
names and a manifest.

Some chapters (e.g. ch01) have NO matplotlib figures — their visuals are regression
tables and mermaid diagrams. That is fine: the manifest is written with an empty
`figures` list and only the visual summary is staged.

The write-slides skill then reads `figures_manifest.json`, picks the load-bearing
figures, and copies the chosen ones into `slides/chNN/figures/`. The deck itself never
executes code — it references the copied images by relative path, so
`quarto render slides.qmd` is a pure Pandoc render.

Figure source (`--source auto` default):
  1. The book-rendered HTML at book/_book/notebooks_quarto/<base>.html, if present
     (reuse — no execution needed; a staleness note prints if the .qmd is newer).
  2. Otherwise (or with `--source render`) re-render the chapter inside the book project:
     `uv run quarto render book/notebooks_quarto/<base>.qmd` (executes the chapter).

Visual summary: the newest `book/images/chNN_visual_summary*.{png,svg,jpg,webp}` is
copied to `<out>/visual_summary.<ext>` (the extension is preserved — SVG is fine).

Usage (from the repo root):
  uv run python .claude/skills/write-slides/scripts/export_chapter_figures.py ch01
  uv run python .../export_chapter_figures.py ch02 --source render   # force a fresh render
  uv run python .../export_chapter_figures.py ch02 --out slides/ch02/_figcache

Output:
  <out>/fig_<nn>.png                 one per chapter figure, document order
  <out>/visual_summary.<ext>         the chapter's visual-summary image (if found)
  <out>/figures_manifest.json        {chapter, source_html, visual_summary, figures: [...]}
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[4]   # scripts → write-slides → skills → .claude → root
BOOK = PROJECT_ROOT / "book"
QUARTO_CMD = ["uv", "run", "quarto"]

# A heading (any level) OR a figure <img> whose src points into a figure-html dir.
TOKEN_RE = re.compile(
    r'<h([1-6])[^>]*>(.*?)</h\1>'
    r'|<img\b[^>]*?\bsrc="([^"]*figure-html/[^"]*\.png)"',
    re.DOTALL | re.IGNORECASE,
)
TAG_RE = re.compile(r"<[^>]+>")
CHID_RE = re.compile(r"^ch(\d{2})$")
SUMMARY_EXTS = (".png", ".svg", ".jpg", ".jpeg", ".webp")


def resolve_chapter_qmd(chid: str) -> Path:
    m = CHID_RE.match(chid)
    if not m:
        sys.exit(f"[export] Chapter id must look like 'ch01', got '{chid}'")
    matches = sorted((BOOK / "notebooks_quarto").glob(f"{m.group(1)}-*.qmd"))
    if not matches:
        sys.exit(f"[export] No chapter .qmd found for '{chid}' in book/notebooks_quarto/")
    return matches[0]


def pick_source_html(qmd: Path, source: str) -> Path:
    """Return the book-rendered chapter HTML (its sibling *_files/figure-html/ holds the PNGs)."""
    book_html = BOOK / "_book" / "notebooks_quarto" / f"{qmd.stem}.html"

    if source == "book" and not book_html.exists():
        sys.exit(f"[export] --source book but {book_html} is missing. Run `uv run quarto render book/`.")
    if source in ("auto", "book") and book_html.exists():
        stale = book_html.stat().st_mtime < qmd.stat().st_mtime
        note = "  (NOTE: chapter .qmd is newer — pass --source render to refresh plots)" if stale else ""
        print(f"[export] Using book-rendered HTML: {book_html.relative_to(PROJECT_ROOT)}{note}")
        return book_html

    # Render fresh inside the book project (source == "render", or no book HTML yet).
    rel = qmd.relative_to(PROJECT_ROOT)
    print(f"[export] Rendering chapter fresh: {' '.join(QUARTO_CMD)} render {rel}")
    try:
        subprocess.run([*QUARTO_CMD, "render", str(rel)], cwd=PROJECT_ROOT, check=True)
    except FileNotFoundError:
        sys.exit("[export] `uv` not found — install uv or run quarto manually.")
    except subprocess.CalledProcessError as e:
        sys.exit(f"[export] quarto render failed (exit {e.returncode}). Run `uv sync` first.")
    if not book_html.exists():
        sys.exit(f"[export] Render produced no HTML at {book_html}")
    return book_html


def rel(p: Path) -> str:
    """Repo-relative path for messages (absolute if outside the repo, e.g. a custom --out)."""
    try:
        return str(p.relative_to(PROJECT_ROOT))
    except ValueError:
        return str(p)


def clean_heading(raw: str) -> str:
    return re.sub(r"\s+", " ", TAG_RE.sub("", raw)).strip()


def parse_figures(html: str):
    """Walk the HTML in document order, tagging each figure with its current heading."""
    current = "intro"
    figs = []
    for m in TOKEN_RE.finditer(html):
        if m.group(2) is not None:               # a heading
            heading = clean_heading(m.group(2))
            if heading and heading.lower() != "table of contents":
                current = heading
        elif m.group(3) is not None:             # a figure img
            figs.append({"src": m.group(3), "heading": current})
    return figs


def copy_visual_summary(chid: str, out: Path):
    candidates = [p for p in (BOOK / "images").glob(f"{chid}_visual_summary*")
                  if p.suffix.lower() in SUMMARY_EXTS]
    if not candidates:
        print(f"[export] WARNING: no visual summary found (book/images/{chid}_visual_summary.*)")
        return None
    chosen = max(candidates, key=lambda p: p.stat().st_mtime)   # newest wins (e.g. a new mind-map PNG)
    for old in out.glob("visual_summary.*"):
        old.unlink()
    dest = out / f"visual_summary{chosen.suffix.lower()}"
    shutil.copy2(chosen, dest)
    print(f"[export] Visual summary: book/images/{chosen.name} → {dest.name}")
    return dest.name


def main():
    ap = argparse.ArgumentParser(description="Stage a chapter's figures for a slide deck.")
    ap.add_argument("chapter", help="chapter id, e.g. ch01")
    ap.add_argument("--out", help="staging dir (default: slides/<chid>/_figcache)")
    ap.add_argument("--source", choices=["auto", "book", "render"], default="auto",
                    help="where figures come from (default: auto)")
    args = ap.parse_args()

    chid = args.chapter
    qmd = resolve_chapter_qmd(chid)
    out = Path(args.out).resolve() if args.out else (PROJECT_ROOT / "slides" / chid / "_figcache")
    out.mkdir(parents=True, exist_ok=True)

    html_path = pick_source_html(qmd, args.source)
    files_dir = html_path.parent
    html = html_path.read_text(encoding="utf-8")

    figs = parse_figures(html)
    manifest = []
    for i, fig in enumerate(figs):
        src_png = (files_dir / fig["src"]).resolve()
        if not src_png.exists():
            print(f"[export] WARNING: figure missing on disk, skipping: {fig['src']}")
            continue
        cache_file = f"fig_{len(manifest) + 1:02d}.png"
        shutil.copy2(src_png, out / cache_file)
        manifest.append({
            "index": i,
            "cache_file": cache_file,
            "src": fig["src"],
            "heading": fig["heading"],
        })

    visual = copy_visual_summary(chid, out)

    manifest_path = out / "figures_manifest.json"
    manifest_path.write_text(json.dumps({
        "chapter": chid,
        "source_html": str(html_path.relative_to(PROJECT_ROOT)),
        "visual_summary": visual,
        "figures": manifest,
    }, indent=2), encoding="utf-8")

    print(f"[export] {len(manifest)} figure(s) staged → {rel(out)}")
    for f in manifest:
        print(f"         {f['cache_file']:12s}  {f['heading']}")
    print(f"[export] Manifest: {rel(manifest_path)}")


if __name__ == "__main__":
    main()
