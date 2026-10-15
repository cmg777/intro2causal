#!/usr/bin/env python3
"""Offline behavioral checks using temporary synthetic fixtures, not generated maps."""

import argparse
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

import artifacts
import check_geometry as geometry


class HelpersTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.run = self.root / "run"
        self.drafts = self.run / "drafts"
        self.drafts.mkdir(parents=True)
        self.source = self.drafts / "selected.png"
        Image.new("RGBA", (120, 80), (15, 23, 42, 255)).save(self.source)
        self.audit = self.run / "audit.json"
        self.audit_data = {"status": "passed", "image_reviewed": True,
                           "source_sha256": artifacts.digest(self.source),
                           "checks": [{"category": c, "status": "pass", "evidence": "test fixture inspected"}
                                      for c in ("content", "numbers", "geometry", "presentation")]}
        self.audit.write_text(json.dumps(self.audit_data))
        self.output = self.root / "images"
        self.manifest = self.run / "export.json"

    def tearDown(self):
        self.temp.cleanup()

    def export_args(self):
        return argparse.Namespace(source=str(self.source), audit=str(self.audit),
                                  output_dir=str(self.output), stem="test-map", manifest=str(self.manifest))

    def test_lossless_export_version_selection_and_archive(self):
        self.output.mkdir()
        (self.output / "test-map-v2.png").write_bytes(b"old master")
        (self.output / "test-map-v10.webp").write_bytes(b"old derivative")
        result = artifacts.export(self.export_args())
        self.assertEqual(result["version"], 11)
        self.assertEqual(artifacts.check_pixels(result["png"], result["webp"]), [120, 80])
        self.assertEqual((self.output / "test-map-v2.png").read_bytes(), b"old master")
        archive = self.root / "batch.zip"
        artifacts.bundle(argparse.Namespace(manifests=[str(self.manifest)], include=[], output=str(archive)))
        with zipfile.ZipFile(archive) as z:
            self.assertIsNone(z.testzip())
            self.assertEqual(len(z.namelist()), 4)
        with self.assertRaises(FileExistsError):
            artifacts.bundle(argparse.Namespace(manifests=[str(self.manifest)], include=[], output=str(archive)))

    def test_failed_or_stale_audit_prevents_export(self):
        for bad in ({"status": "incomplete"}, {"source_sha256": "wrong"}, {"image_reviewed": False}):
            self.audit.write_text(json.dumps({**self.audit_data, **bad}))
            with self.assertRaises(ValueError):
                artifacts.export(self.export_args())
            self.assertFalse(self.output.exists())

    def test_cleanup_preflights_all_files_and_preserves_evidence(self):
        artifacts.export(self.export_args())
        extra = self.drafts / "old.png"
        Image.new("RGB", (10, 10)).save(extra)
        outside = self.root / "another-run.png"
        outside.write_bytes(b"keep")
        args = argparse.Namespace(manifest=str(self.manifest), draft_root=str(self.drafts),
                                  files=[str(extra), str(outside)])
        with self.assertRaises(ValueError):
            artifacts.cleanup(args)
        self.assertTrue(extra.exists())
        self.assertTrue(outside.exists())
        args.files = [str(extra), str(self.audit)]
        with self.assertRaises(ValueError):
            artifacts.cleanup(args)
        self.assertTrue(extra.exists())
        args.files = [str(extra), str(self.source)]
        artifacts.cleanup(args)
        self.assertFalse(extra.exists())
        self.assertFalse(self.source.exists())
        self.assertTrue(self.audit.exists())
        artifacts.checked_export(self.manifest)

    def test_changed_export_prevents_cleanup(self):
        result = artifacts.export(self.export_args())
        Path(result["png"]).write_bytes(b"corrupt")
        with self.assertRaises(ValueError):
            artifacts.cleanup(argparse.Namespace(manifest=str(self.manifest), draft_root=str(self.drafts), files=[str(self.source)]))
        self.assertTrue(self.source.exists())

    def test_raster_parallel_and_nonparallel_lines(self):
        img = Image.new("RGB", (200, 140), (15, 23, 42))
        draw = ImageDraw.Draw(img)
        draw.line((20, 40, 180, 40), fill=(56, 189, 248), width=3)
        draw.line((20, 90, 180, 90), fill=(167, 139, 250), width=3)
        row = {"type": "parallel_lines", "xs": [40, 70, 100, 130, 160],
               "line_a": {"y_range": [20, 65], "rgb": [56, 189, 248]},
               "line_b": {"y_range": [65, 125], "rgb": [167, 139, 250]}}
        self.assertTrue(geometry.check(row, np.array(img))["passed"])
        draw.rectangle((15, 65, 185, 125), fill=(15, 23, 42))
        draw.line((20, 110, 180, 75), fill=(167, 139, 250), width=3)
        self.assertFalse(geometry.check(row, np.array(img))["passed"])
        row["line_b"]["rgb"] = [255, 0, 0]
        with self.assertRaises(ValueError):
            geometry.check(row, np.array(img))

    def test_landmark_constraints(self):
        pixels = np.zeros((200, 200, 3), dtype=np.uint8)
        common = {"measurement_method": "known synthetic fixture landmarks", "tolerance_px": 1}
        interval = {**common, "type": "symmetric_interval", "left": [20, 40], "right": [180, 40], "estimate": [100, 40]}
        self.assertTrue(geometry.check(interval, pixels)["passed"])
        interval["estimate"] = [120, 40]
        self.assertFalse(geometry.check(interval, pixels)["passed"])
        windows = {**common, "type": "centered_windows", "cutoff_x": 100, "narrow": [80, 120], "wide": [50, 150]}
        self.assertTrue(geometry.check(windows, pixels)["passed"])
        windows["wide"] = [100, 190]
        self.assertFalse(geometry.check(windows, pixels)["passed"])
        jump = {**common, "type": "jump_fraction", "zero": [20, 150], "one": [20, 50],
                "before": [100, 120], "after": [100, 80], "expected_fraction": .4}
        self.assertTrue(geometry.check(jump, pixels)["passed"])
        jump["after"] = [100, 40]
        self.assertFalse(geometry.check(jump, pixels)["passed"])
        aligned = {**common, "type": "same_coordinate", "axis": "x", "points": [[100, 40], [100, 90]]}
        self.assertTrue(geometry.check(aligned, pixels)["passed"])
        aligned["points"][1][0] = 120
        self.assertFalse(geometry.check(aligned, pixels)["passed"])


if __name__ == "__main__":
    unittest.main()
