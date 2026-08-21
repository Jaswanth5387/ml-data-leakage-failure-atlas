# ML Data Leakage Failure Atlas v0.1.0

This is the first reviewed release of the ML Data Leakage Failure Atlas, an evidence-first dataset of leakage found in real public machine-learning work and primary research sources.

## Included in this release

- 18 verified cases at immutable source revisions.
- 20 screened sources: 15 public GitHub artifacts and five primary research papers.
- Two negative screening results retained in the source manifest.
- Five leakage mechanisms: preprocessing, evaluation, contamination, temporal, and target leakage.
- Five cases with controlled impact comparisons reported by their primary sources.
- Machine-readable indexes, a case schema, evidence rules, methodology, automated validation, and tests.

## Important limitation

This is a targeted discovery corpus, not a random sample. The case counts describe this release only and must not be used as estimates of how common data leakage is across machine-learning projects.

The five `source_measured` cases contain controlled comparisons reported by their primary sources. The atlas has not independently reproduced those experiments. The other 13 impact assessments are explicitly marked `inferred`.

## Validation

Run:

```bash
python scripts/validate_cases.py
python -m unittest discover -s tests -v
python scripts/check_release.py 0.1.0
```

Dataset metadata and original annotations are licensed under CC BY 4.0. Validation and summary code are licensed under MIT. Third-party sources retain their original copyrights and licenses.
