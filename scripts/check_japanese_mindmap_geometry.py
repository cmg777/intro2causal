"""Check the generated DD diagrams' parallel pre-treatment lines.

Uses the native approved raster images without modifying them. Fixed windows
identify the schematic lines, not text or empirical observations. These checks
complement manual diagram review; they cannot establish causal assumptions.
Run: uv run python scripts/check_japanese_mindmap_geometry.py
"""
from pathlib import Path
from statistics import median
import json
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


def sample_rows(im, xs, y0, y1, color):
    rows = []
    for x in xs:
        hits = []
        for y in range(y0, y1):
            for dx in [-1, 0, 1]:
                r, g, b = im.getpixel((x + dx, y))
                match = r < 120 and g > 130 and b > 120 if color == 'cyan' else r > 140 and b > 180 and g < 160
                if match:
                    hits.append(y)
        assert hits, f'No {color} line at x={x}'
        rows.append(median(hits))
    return rows


def verify():
    cases = [
        ('chapter_5', 'ch05-differences-in-differences-v1.png', [100, 125, 150, 175, 200], (590, 610), (630, 650)),
        ('chapter_6', 'ch06-wages-of-schooling-v1.png', [1085, 1100, 1120, 1140, 1160], (526, 542), (572, 588)),
    ]
    actual = {}
    for name, file, xs, treated_window, control_window in cases:
        im = Image.open(ROOT / 'mindmaps/ja/images' / file).convert('RGB')
        treated = sample_rows(im, xs, *treated_window, 'cyan')
        control = sample_rows(im, xs, *control_window, 'purple')
        separation = [b-a for a, b in zip(treated, control)]
        # Hand-ink strokes can differ by a few pixels. Positive separation in
        # raster coordinates means treated is above control at every sample.
        assert min(separation) > 0, name
        assert max(treated)-min(treated) <= 3, name
        assert max(control)-min(control) <= 3, name
        assert max(separation)-min(separation) <= 3, name
        actual[name] = {'x_pixels': xs, 'treated_y_pixels': treated, 'control_y_pixels': control, 'separation_drift_pixels': max(separation)-min(separation), 'passed': True}
    recorded = json.loads((ROOT / 'mindmaps/ja/review/geometry-checks.json').read_text())
    assert actual == recorded['checks'], 'Recorded geometry differs from selected images'
    print('PASS: both DD diagrams retain parallel pre-trends at different levels')


if __name__ == '__main__':
    verify()
