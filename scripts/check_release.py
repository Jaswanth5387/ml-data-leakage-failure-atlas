#!/usr/bin/env python3
"""Check that release metadata agrees on one version."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")


def extract(pattern: str, text: str, source: str) -> str:
    match = re.search(pattern, text, flags=re.MULTILINE)
    if not match:
        raise ValueError(f"{source}: required metadata was not found")
    return match.group(1)


def check_release(expected: str) -> list[str]:
    errors: list[str] = []
    if not SEMVER.fullmatch(expected):
        return [f"expected version must be SemVer without a leading v: {expected!r}"]

    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    citation = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    zenodo = json.loads((ROOT / ".zenodo.json").read_text(encoding="utf-8"))

    versions = {
        "pyproject.toml": extract(r'^version\s*=\s*"([^"]+)"', pyproject, "pyproject.toml"),
        "CITATION.cff": extract(r"^version:\s*[\"']?([^\s\"']+)", citation, "CITATION.cff"),
        ".zenodo.json": str(zenodo.get("version", "")),
    }
    for source, actual in versions.items():
        if actual != expected:
            errors.append(f"{source}: version is {actual!r}; expected {expected!r}")

    if not re.search(rf"^## \[{re.escape(expected)}\] - \d{{4}}-\d{{2}}-\d{{2}}$", changelog, re.MULTILINE):
        errors.append(f"CHANGELOG.md: missing dated [{expected}] release heading")

    if zenodo.get("upload_type") != "dataset":
        errors.append(".zenodo.json: upload_type must be 'dataset'")
    if zenodo.get("license") != "cc-by-4.0":
        errors.append(".zenodo.json: license must be 'cc-by-4.0'")
    if not zenodo.get("creators"):
        errors.append(".zenodo.json: at least one creator is required")
    if "doi:" in citation.lower():
        doi = extract(r"^doi:\s*(\S+)", citation, "CITATION.cff")
        if "PLACEHOLDER" in doi.upper() or "TBD" in doi.upper():
            errors.append("CITATION.cff: DOI must not be a placeholder")

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: python scripts/check_release.py VERSION", file=sys.stderr)
        return 2

    errors = check_release(sys.argv[1])
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"Release metadata is consistent for {sys.argv[1]}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
