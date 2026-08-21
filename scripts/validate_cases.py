#!/usr/bin/env python3
"""Validate the atlas CSV indexes and case-file links using the standard library."""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
CASE_COLUMNS = [
    "case_id", "title", "status", "confidence", "primary_mechanism", "subtype",
    "source_type", "source_url", "source_revision", "reproduction_status",
    "impact_basis", "case_file",
]
SOURCE_COLUMNS = [
    "source_id", "competition", "notebook_slug", "notebook_version", "source_url",
    "collected_at_utc", "license", "screening_status", "duplicate_group", "notes",
]
ALLOWED = {
    "status": {"candidate", "under_review", "verified", "disputed", "withdrawn"},
    "confidence": {"confirmed", "probable", "ambiguous"},
    "primary_mechanism": {"target", "temporal", "preprocessing", "contamination"},
    "source_type": {"kaggle", "github", "paper"},
    "reproduction_status": {"reproduced", "partially_reproduced", "static_verified", "not_reproduced", "not_attempted"},
    "impact_basis": {"measured", "inferred", "unknown"},
}


def read_rows(path: Path, expected: list[str]) -> tuple[list[dict[str, str]], list[str]]:
    errors: list[str] = []
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != expected:
            errors.append(f"{path.relative_to(ROOT)}: expected columns {expected}, got {reader.fieldnames}")
        rows = list(reader)
    return rows, errors


def valid_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc)


def validate(root: Path = ROOT) -> list[str]:
    global ROOT
    previous_root = ROOT
    ROOT = root
    try:
        rows, errors = read_rows(root / "data/cases.csv", CASE_COLUMNS)
        _, source_errors = read_rows(root / "corpus/sources.csv", SOURCE_COLUMNS)
        errors.extend(source_errors)
        seen: set[str] = set()
        for number, row in enumerate(rows, start=2):
            prefix = f"data/cases.csv:{number}"
            case_id = row.get("case_id", "")
            if not re.fullmatch(r"MLA-\d{3}", case_id):
                errors.append(f"{prefix}: invalid case_id {case_id!r}")
            if case_id in seen:
                errors.append(f"{prefix}: duplicate case_id {case_id}")
            seen.add(case_id)
            for field, allowed in ALLOWED.items():
                if row.get(field) not in allowed:
                    errors.append(f"{prefix}: invalid {field} {row.get(field)!r}")
            if not valid_url(row.get("source_url", "")):
                errors.append(f"{prefix}: source_url must be an https URL")
            case_file = row.get("case_file", "")
            if not re.fullmatch(r"cases/MLA-\d{3}[-_].+\.md", case_file):
                errors.append(f"{prefix}: invalid case_file {case_file!r}")
            elif not (root / case_file).is_file():
                errors.append(f"{prefix}: missing {case_file}")
            if row.get("status") == "verified" and row.get("confidence") == "ambiguous":
                errors.append(f"{prefix}: verified cases cannot be ambiguous")
            if row.get("impact_basis") == "measured" and row.get("reproduction_status") != "reproduced":
                errors.append(f"{prefix}: measured impact requires reproduction_status=reproduced")
        return errors
    finally:
        ROOT = previous_root


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    errors = validate()
    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Atlas validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

