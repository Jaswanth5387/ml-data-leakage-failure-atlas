#!/usr/bin/env python3
"""Print conservative counts from the case index."""

import csv
from collections import Counter
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "data/cases.csv"
with path.open(newline="", encoding="utf-8") as handle:
    rows = list(csv.DictReader(handle))

verified = [row for row in rows if row["status"] == "verified" and row["confidence"] in {"confirmed", "probable"}]
print(f"Indexed cases: {len(rows)}")
print(f"Verified cases: {len(verified)}")
for mechanism, count in sorted(Counter(row["primary_mechanism"] for row in verified).items()):
    print(f"{mechanism}: {count}")

