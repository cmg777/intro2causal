#!/usr/bin/env python3
"""sync_mindmap_images.py — publish the chapter mind-map images to the book and the decks.

Source of truth: `mindmaps/images/chNN-<slug>-vN.png` (drawn in a separate app; never
modified here). For every chapter that has an image — the highest `-vN` wins — this:

  1. writes a compressed WebP copy and samples the image's edge colour;
  2. book:  book/images/chNN_visual_summary.webp, points the chapter .qmd at it, and deletes
            the old concept card (book/images/chNN_visual_summary.svg);
  3. deck:  slides/chNN/figures/visual_summary.webp, rewrites `visual-summary:` +
            `visual-summary-bg:` in the front matter and the Recap slide's background,
            re-copies the title-slide template, deletes figures/visual_summary.svg,
            re-renders the deck and runs the smoke test;
  4. re-renders the book once and checks each updated chapter page uses the WebP.

Chapters without an image are skipped and reported. Re-running is safe (a new -v2 simply
replaces the WebP). Commit afterwards.

Usage (from the repo root):
  uv run python .claude/skills/write-slides/scripts/sync_mindmap_images.py
  uv run python .claude/skills/write-slides/scripts/sync_mindmap_images.py --dry-run
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from mindmap_image import PROJECT_ROOT, latest_mindmap_image, write_webp

BOOK = PROJECT_ROOT / "book"
SLIDES = PROJECT_ROOT / "slides"
TEMPLATES = Path(__file__).resolve().parents[1] / "references" / "templates"
CHAPTERS = [f"ch{n:02d}" for n in range(1, 7)]

# The `visual-summary:` line plus its indented continuation comments, and any old `-bg` line.
VS_RE = re.compile(r'^visual-summary:.*\n(?:[ \t]+#.*\n)*(?:visual-summary-bg:.*\n)?', re.MULTILINE)
RECAP_RE = re.compile(r'^(## \{\.recap\b[^}\n]*\})', re.MULTILINE)


def run(cmd, cwd, env=None) -> bool:
    print(f"  $ {' '.join(cmd)}   (in {cwd.relative_to(PROJECT_ROOT) or '.'})")
    return subprocess.run(cmd, cwd=cwd, env=env).returncode == 0


def update_book_qmd(chid: str) -> Path:
    qmd = next((BOOK / "notebooks_quarto").glob(f"{chid[2:]}-*.qmd"))
    text = qmd.read_text(encoding="utf-8")
    new = re.sub(rf'(\.\./images/{chid}_visual_summary)\.\w+', r'\1.webp', text)
    if f"../images/{chid}_visual_summary.webp" not in new:
        raise RuntimeError(f"{qmd.name}: no visual-summary image reference to update")
    qmd.write_text(new, encoding="utf-8")
    return qmd


def update_deck_qmd(qmd: Path, bg: str):
    text = qmd.read_text(encoding="utf-8")
    front = (f'visual-summary: "figures/visual_summary.webp"   # mind-map image, synced from mindmaps/images;\n'
             f'                                                # the Recap slide repeats this path\n'
             f'visual-summary-bg: "{bg}"                     # its edge colour: letterbox on non-16:9 screens\n')
    text, n = VS_RE.subn(front, text, count=1)
    if n != 1:
        raise RuntimeError(f"{qmd}: no `visual-summary:` front-matter line")

    def recap(m):
        h = re.sub(r'background-image="[^"]*"', 'background-image="figures/visual_summary.webp"', m.group(1))
        return re.sub(r'background-color="[^"]*"', f'background-color="{bg}"', h)

    text, n = RECAP_RE.subn(recap, text, count=1)
    if n != 1:
        raise RuntimeError(f"{qmd}: no `## {{.recap …}}` slide")
    qmd.write_text(text, encoding="utf-8")


def remove_old(paths):
    for p in paths:
        if p.exists():
            p.unlink()
            print(f"  removed {p.relative_to(PROJECT_ROOT)}")


def main():
    ap = argparse.ArgumentParser(description="Publish mind-map images to the book and the decks.")
    ap.add_argument("--dry-run", action="store_true",
                    help="report what would change (WebPs built in a temp dir); touch nothing")
    args = ap.parse_args()

    rows, failed, updated = [], False, []
    tmp = Path(tempfile.mkdtemp(prefix="mindmap_webp_")) if args.dry_run else None

    for chid in CHAPTERS:
        src, ver = latest_mindmap_image(chid)
        if src is None:
            rows.append((chid, "—", "—", "skipped (no image)", "", ""))
            continue
        print(f"\n[{chid}] {src.relative_to(PROJECT_ROOT)}")
        deck = SLIDES / chid
        has_deck = (deck / "slides.qmd").exists()

        if args.dry_run:
            bg = write_webp(src, tmp / f"{chid}.webp")
            size = f"{(tmp / f'{chid}.webp').stat().st_size // 1024} KB"
            rows.append((chid, f"v{ver}", size, f"would sync (bg {bg})",
                         "deck" if has_deck else "no deck", "book"))
            continue

        # Book: WebP + chapter reference; drop the old concept card.
        book_img = BOOK / "images" / f"{chid}_visual_summary.webp"
        bg = write_webp(src, book_img)
        update_book_qmd(chid)
        remove_old([p for p in (BOOK / "images").glob(f"{chid}_visual_summary.*") if p != book_img])
        size = f"{book_img.stat().st_size // 1024} KB"

        deck_ok = smoke_ok = "no deck"
        if has_deck:
            fig = deck / "figures" / "visual_summary.webp"
            shutil.copy2(book_img, fig)
            update_deck_qmd(deck / "slides.qmd", bg)
            shutil.copy2(TEMPLATES / "title-slide.html", deck / "title-slide.html")
            remove_old([p for p in (deck / "figures").glob("visual_summary.*") if p != fig])
            rendered = run(["uv", "run", "quarto", "render", "slides.qmd"], deck)
            smoke = rendered and run(["node", str(TEMPLATES / "smoke-test.js")], PROJECT_ROOT,
                                     env={**os.environ, "BASE": str(deck)})
            deck_ok, smoke_ok = ("✓" if rendered else "✗"), ("✓" if smoke else "✗")
            failed |= not (rendered and smoke)
        updated.append(chid)
        rows.append((chid, f"v{ver}", size, f"synced (bg {bg})", f"deck {deck_ok} smoke {smoke_ok}", ""))

    if updated:
        print("\n[book] re-rendering the book …")
        book_ok = run(["uv", "run", "quarto", "render", "book/"], PROJECT_ROOT)
        failed |= not book_ok
        for i, row in enumerate(rows):
            if row[0] in updated:
                html = next((BOOK / "_book" / "notebooks_quarto").glob(f"{row[0][2:]}-*.html"))
                ok = book_ok and f"{row[0]}_visual_summary.webp" in html.read_text(encoding="utf-8")
                failed |= not ok
                rows[i] = (*row[:5], f"book {'✓' if ok else '✗'}")

    print("\nMIND-MAP SYNC" + (" (dry run — nothing changed)" if args.dry_run else ""))
    for r in rows:
        print("  " + "  ".join(f"{c:<{w}}" for c, w in zip(r, (5, 4, 8, 28, 20, 8))).rstrip())
    if updated:
        print("\nNext: review, then commit slides/ book/ (incl. book/_book/ and the deleted SVGs).")
    if tmp:
        shutil.rmtree(tmp, ignore_errors=True)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
