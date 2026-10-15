#!/usr/bin/env python3
"""Check raster-sampled lines and measured landmarks; does not audit semantics."""

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image


def finite(value):
    a = np.asarray(value, dtype=float)
    if not np.isfinite(a).all():
        raise ValueError("Measurements must be finite")
    return a


def point(value, shape):
    a = finite(value)
    if a.shape != (2,) or not (0 <= a[0] < shape[1] and 0 <= a[1] < shape[0]):
        raise ValueError("Landmark must be [x,y] inside the native image")
    return a


def sample_line(pixels, xs, config):
    y0, y1 = config["y_range"]
    if not (isinstance(y0, int) and isinstance(y1, int) and 0 <= y0 < y1 <= pixels.shape[0]):
        raise ValueError("Invalid line sampling y_range")
    target = finite(config["rgb"])
    if target.shape != (3,) or (target < 0).any() or (target > 255).any():
        raise ValueError("Expected RGB color in [0,255]")
    tolerance = float(config.get("color_tolerance", 60))
    if not 0 < tolerance <= 150:
        raise ValueError("Invalid color tolerance")
    ys = []
    for x in xs:
        if not isinstance(x, int) or not 0 <= x < pixels.shape[1]:
            raise ValueError("Sampling x must be an integer inside the image")
        strip = pixels[y0:y1, max(0, x-1):min(pixels.shape[1], x+2), :].astype(float)
        mask = np.linalg.norm(strip-target, axis=2) <= tolerance
        rows = np.where(mask)[0]
        if not len(rows):
            raise ValueError(f"No line color at x={x}; inspect the region")
        ys.append(float(np.median(rows)+y0))
    return np.asarray(ys)


def check(row, pixels):
    kind = row["type"]
    if kind == "parallel_lines":
        xs = row["xs"]
        if len(xs) < 3 or xs != sorted(set(xs)):
            raise ValueError("Use at least three distinct increasing sample x positions")
        a = sample_line(pixels, xs, row["line_a"])
        b = sample_line(pixels, xs, row["line_b"])
        sa, sb = float(np.polyfit(xs, a, 1)[0]), float(np.polyfit(xs, b, 1)[0])
        drift = float(np.ptp(b-a))
        passed = drift <= row.get("max_separation_drift_px", 3) and abs(sa-sb) <= row.get("max_slope_difference", .02)
        return {"passed": bool(passed), "xs": xs, "line_a_ys": a.tolist(),
                "line_b_ys": b.tolist(), "slopes": [sa, sb], "separation_drift_px": drift}
    if not str(row.get("measurement_method", "")).strip():
        raise ValueError("Manual landmarks need measurement_method evidence")
    tol = float(row.get("tolerance_px", 3))
    if not np.isfinite(tol) or tol < 0:
        raise ValueError("Invalid pixel tolerance")
    if kind == "symmetric_interval":
        left, right, center = [point(row[k], pixels.shape) for k in ("left", "right", "estimate")]
        if right[0] <= left[0]:
            raise ValueError("Interval endpoints are reversed")
        err = float(np.linalg.norm(center-(left+right)/2))
        flat = abs(float(right[1]-left[1]))
        return {"passed": err <= tol and flat <= tol, "centering_error_px": err, "endpoint_y_difference_px": flat}
    if kind == "centered_windows":
        cutoff = float(finite(row["cutoff_x"]))
        if not 0 <= cutoff < pixels.shape[1]:
            raise ValueError("Cutoff is outside the image")
        windows = finite([row["narrow"], row["wide"]])
        if windows.shape != (2, 2) or (windows[:, 1] <= windows[:, 0]).any():
            raise ValueError("Window endpoints must increase")
        if (windows < 0).any() or (windows >= pixels.shape[1]).any():
            raise ValueError("Window endpoints are outside the image")
        errors = abs(windows.mean(axis=1)-cutoff)
        nested = windows[1, 0] <= windows[0, 0] < windows[0, 1] <= windows[1, 1]
        return {"passed": bool(nested and (errors <= tol).all()), "center_errors_px": errors.tolist(), "nested": bool(nested)}
    if kind == "jump_fraction":
        zero, one, before, after = [point(row[k], pixels.shape) for k in ("zero", "one", "before", "after")]
        height = float(zero[1]-one[1])
        expected = float(row["expected_fraction"])
        fraction_tol = float(row.get("fraction_tolerance", .03))
        if height <= 0 or not -1 <= expected <= 1 or not 0 <= fraction_tol <= .1:
            raise ValueError("Invalid probability-axis scale or fraction")
        p0, p1 = (zero[1]-before[1])/height, (zero[1]-after[1])/height
        frac = float(p1-p0)
        bounded = -tol/height <= min(p0, p1) and max(p0, p1) <= 1+tol/height
        aligned = abs(float(before[0]-after[0])) <= tol
        return {"passed": bool(bounded and aligned and abs(frac-expected) <= fraction_tol),
                "measured_fraction": frac, "levels": [float(p0), float(p1)], "same_cutoff": aligned}
    if kind == "same_coordinate":
        axis = {"x": 0, "y": 1}[row.get("axis", "x")]
        pts = np.asarray([point(p, pixels.shape) for p in row["points"]])
        if len(pts) < 2:
            raise ValueError("Need at least two landmarks")
        spread = float(np.ptp(pts[:, axis]))
        return {"passed": spread <= tol, "coordinate_spread_px": spread}
    raise ValueError(f"Unsupported geometry type: {kind}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image")
    parser.add_argument("--checks", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    image = Path(args.image)
    pixels = np.array(Image.open(image).convert("RGB"))
    config = json.loads(Path(args.checks).read_text(encoding="utf-8"))
    if not config.get("checks"):
        parser.error("No checks supplied; absence of checks is not a pass")
    rows = []
    for row in config["checks"]:
        try:
            result = check(row, pixels)
        except (ValueError, KeyError, TypeError, IndexError) as e:
            result = {"passed": False, "error": str(e)}
        rows.append({"id": row.get("id"), "type": row.get("type"), **result})
    passed = all(r["passed"] for r in rows)
    output = {"image": str(image.resolve()), "image_sha256": hashlib.sha256(image.read_bytes()).hexdigest(),
              "dimensions": [pixels.shape[1], pixels.shape[0]], "passed": passed,
              "checks": rows, "scope": "Pixel sampling and supplied landmarks only; semantic audit is separate."}
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(output, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(output, indent=2))
    raise SystemExit(0 if passed else 1)


if __name__ == "__main__":
    main()
