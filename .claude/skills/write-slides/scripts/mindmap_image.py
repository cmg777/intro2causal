"""mindmap_image.py — shared helpers for the chapter mind-map images.

The finished mind-map images are drawn in a separate app and saved, untouched, as
`mindmaps/images/chNN-<slug>-vN.png` (16:9). These helpers pick the highest version for a
chapter, write a compressed WebP copy for the web (book + decks), and sample the image's
border colour so letterbox bars on non-16:9 screens blend into the image.

Used by sync_mindmap_images.py (publishes the images) and export_chapter_figures.py
(stages the visual summary for a new deck).
"""

import re
from pathlib import Path

from PIL import Image

PROJECT_ROOT = Path(__file__).resolve().parents[4]   # scripts → write-slides → skills → .claude → root
MINDMAP_IMAGES = PROJECT_ROOT / "mindmaps" / "images"
VERSION_RE = re.compile(r"-v(\d+)\.png$", re.IGNORECASE)
WEBP_QUALITY = 85


def latest_mindmap_image(chid: str):
    """Return (path, version) of the highest-version `chNN-*-vN.png`, or (None, None)."""
    best = (None, None)
    for p in MINDMAP_IMAGES.glob(f"{chid}-*-v*.png"):
        m = VERSION_RE.search(p.name)
        if m and (best[1] is None or int(m.group(1)) > best[1]):
            best = (p, int(m.group(1)))
    return best


def edge_color(img: Image.Image) -> str:
    """Mean colour of the 1-px border, as #rrggbb — the letterbox colour."""
    rgb = img.convert("RGB")
    w, h = rgb.size
    px = rgb.load()
    border = [px[x, 0] for x in range(w)] + [px[x, h - 1] for x in range(w)]
    border += [px[0, y] for y in range(h)] + [px[w - 1, y] for y in range(h)]
    r, g, b = (round(sum(c[i] for c in border) / len(border)) for i in range(3))
    return f"#{r:02x}{g:02x}{b:02x}"


def write_webp(src: Path, dest: Path) -> str:
    """Write a full-size, high-quality WebP copy of `src`; return the image's edge colour."""
    with Image.open(src) as img:
        dest.parent.mkdir(parents=True, exist_ok=True)
        img.convert("RGB").save(dest, "WEBP", quality=WEBP_QUALITY, method=6)
        return edge_color(img)
