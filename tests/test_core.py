from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from file_organizer.core import build_plan, classify_path


class ClassifyPathTests(unittest.TestCase):
    def test_classifies_known_extension(self) -> None:
        category, reason = classify_path(Path("report.pdf"))

        self.assertEqual(category, "Documents")
        self.assertIn(".pdf", reason)

    def test_unknown_extension_goes_to_other(self) -> None:
        category, reason = classify_path(Path("mystery.custom"))

        self.assertEqual(category, "Other")
        self.assertEqual(reason, "no extension rule matched")


class BuildPlanTests(unittest.TestCase):
    def test_builds_plan_for_top_level_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            (root / "photo.jpg").write_text("image")
            (root / "notes.txt").write_text("notes")
            (root / "nested").mkdir()
            (root / "nested" / "clip.mp4").write_text("video")

            plan = build_plan(root)

            destinations = {item.destination.relative_to(root) for item in plan}
            self.assertEqual(destinations, {Path("Images/photo.jpg"), Path("Documents/notes.txt")})

    def test_recursive_scan_includes_nested_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            (root / "nested").mkdir()
            (root / "nested" / "clip.mp4").write_text("video")

            plan = build_plan(root, recursive=True)

            self.assertEqual(len(plan), 1)
            self.assertEqual(plan[0].destination.relative_to(root), Path("Video/clip.mp4"))

    def test_hidden_files_are_skipped_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            (root / ".secret.pdf").write_text("hidden")

            plan = build_plan(root)

            self.assertEqual(plan, [])

    def test_can_include_hidden_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            (root / ".secret.pdf").write_text("hidden")

            plan = build_plan(root, include_hidden=True)

            self.assertEqual(len(plan), 1)
            self.assertEqual(plan[0].destination.relative_to(root), Path("Documents/.secret.pdf"))

    def test_conflicting_destinations_are_renamed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            (root / "Documents").mkdir()
            (root / "Documents" / "report.pdf").write_text("existing")
            (root / "report.pdf").write_text("new")

            plan = build_plan(root)

            self.assertEqual(len(plan), 1)
            self.assertEqual(plan[0].destination.relative_to(root), Path("Documents/report (1).pdf"))


if __name__ == "__main__":
    unittest.main()
