import csv
import tempfile
import unittest
from pathlib import Path

from scripts.validate_cases import CASE_COLUMNS, SOURCE_COLUMNS, validate


def write_csv(path: Path, columns: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


class ValidatorTests(unittest.TestCase):
    def test_repository_indexes_are_valid(self):
        self.assertEqual(validate(), [])

    def make_root(self) -> Path:
        root = Path(tempfile.mkdtemp())
        write_csv(root / "corpus/sources.csv", SOURCE_COLUMNS, [])
        (root / "cases").mkdir()
        return root

    def test_empty_indexes_are_valid(self):
        root = self.make_root()
        write_csv(root / "data/cases.csv", CASE_COLUMNS, [])
        self.assertEqual(validate(root), [])

    def test_verified_ambiguous_case_is_rejected(self):
        root = self.make_root()
        case_file = root / "cases/MLA-001_example.md"
        case_file.write_text("# evidence\n", encoding="utf-8")
        row = dict.fromkeys(CASE_COLUMNS, "value")
        row.update({
            "case_id": "MLA-001", "title": "Example leakage case", "status": "verified",
            "confidence": "ambiguous", "primary_mechanism": "preprocessing",
            "source_type": "kaggle", "source_url": "https://example.com/notebook/1",
            "reproduction_status": "static_verified", "impact_basis": "unknown",
            "case_file": "cases/MLA-001_example.md",
        })
        write_csv(root / "data/cases.csv", CASE_COLUMNS, [row])
        self.assertTrue(any("cannot be ambiguous" in error for error in validate(root)))

    def test_measured_impact_requires_reproduction(self):
        root = self.make_root()
        case_file = root / "cases/MLA-002_example.md"
        case_file.write_text("# evidence\n", encoding="utf-8")
        row = dict.fromkeys(CASE_COLUMNS, "value")
        row.update({
            "case_id": "MLA-002", "title": "Another leakage case", "status": "candidate",
            "confidence": "probable", "primary_mechanism": "temporal",
            "source_type": "github", "source_url": "https://example.com/repo/commit",
            "reproduction_status": "not_attempted", "impact_basis": "measured",
            "case_file": "cases/MLA-002_example.md",
        })
        write_csv(root / "data/cases.csv", CASE_COLUMNS, [row])
        self.assertTrue(any("measured impact requires" in error for error in validate(root)))


if __name__ == "__main__":
    unittest.main()
