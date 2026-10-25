"""Export the approved Spanish chapter mind maps to WebP and record their provenance.

Run with: uv run python scripts/export_spanish_mindmaps.py
Native PNGs in mindmaps/es/images/ are kept unchanged; only RGB conversion and WebP
encoding are applied. No resizing or upscaling.
"""
import hashlib
import json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
IMAGES = ROOT / 'mindmaps/es/images'
WEB = ROOT / 'assets/home-es/full'
CHAPTERS = {
    1: ('ch01-randomized-trials', 'v1'),
    2: ('ch02-regression', 'v2'),
    3: ('ch03-instrumental-variables', 'v1'),
    4: ('ch04-regression-discontinuity', 'v3'),
    5: ('ch05-differences-in-differences', 'v2'),
    6: ('ch06-wages-of-schooling', 'v2'),
}


def file_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    WEB.mkdir(parents=True, exist_ok=True)
    chapters = []
    for number, (slug, version) in CHAPTERS.items():
        native = IMAGES / f'{slug}-{version}.png'
        web = WEB / f'{slug}-{version}.webp'
        source = ROOT / f'book/images/ch0{number}_visual_summary.webp'
        with Image.open(native) as image:
            width, height = image.size
            image.convert('RGB').save(web, 'WEBP', quality=90, method=6)
        prompts = sorted(p.relative_to(ROOT).as_posix() for p in (ROOT / 'mindmaps/es/prompts').glob(f'{slug}-*.txt'))
        chapters.append({
            'chapter': number, 'slug': slug, 'version': version,
            'english_source': source.relative_to(ROOT).as_posix(), 'english_source_sha256': file_hash(source),
            'full_image': native.relative_to(ROOT).as_posix(), 'full_image_sha256': file_hash(native),
            'web_image': web.relative_to(ROOT).as_posix(), 'web_image_sha256': file_hash(web),
            'native_width': width, 'native_height': height, 'upscaled': False,
            'prompts': ['mindmaps/es/prompts/_common.txt', *prompts],
            'generator': 'Codex CLI built-in image_gen',
        })
    manifest = {
        'schema_version': 1, 'language': 'es', 'variety': 'neutral Latin American Spanish (tú)',
        'review': 'Manual visual comparison of each image against the complete English source and the exact '
                  'Spanish prompt: every branch, bullet, label, equation, number and diagram direction. '
                  'Spelling defects were corrected with targeted edit passes (v2/v3); see the *-fix.txt prompts.',
        'chapters': chapters,
    }
    (ROOT / 'mindmaps/es/manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    for item in chapters:
        print(item['web_image'], item['native_width'], 'x', item['native_height'])


if __name__ == '__main__':
    main()
