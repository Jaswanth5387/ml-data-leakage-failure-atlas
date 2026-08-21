# ML Data Leakage Failure Atlas

An evidence-first catalog of data leakage found in real, publicly accessible machine-learning projects.

This repository is a research artifact, not a collection of textbook examples. Every accepted case must point to a stable public source, identify the exact leaking code or data operation, explain the violated evaluation boundary, and record how the finding was checked.

> **Project status:** foundation / candidate collection. There are currently **0 verified cases**. Counts will only increase after evidence review. Empty data files are intentional; no cases have been invented to make the atlas look complete.

## Research question

How does data leakage appear in public ML work, how strong is the available evidence, and what changes when the leaking pipeline is corrected?

## Initial bounded corpus

The first study targets public Kaggle notebooks associated with five competition ecosystems:

- Home Credit Default Risk
- IEEE-CIS Fraud Detection
- M5 Forecasting — Accuracy
- Store Sales — Time Series Forecasting
- Histopathologic Cancer Detection

The frozen notebook/version list—not a changing search result—is the actual corpus. It will live in [`corpus/sources.csv`](corpus/sources.csv). Selection and stopping rules are in [`docs/methodology.md`](docs/methodology.md).

## What qualifies as a case

A case must include:

1. a real, citable public source and stable revision identifier;
2. exact evidence showing information crossing the intended train/evaluation boundary;
3. a mechanism and subtype from the taxonomy;
4. a confidence label: `confirmed`, `probable`, or `ambiguous`;
5. a correction or mitigation;
6. a reproducibility record, including failures and access limitations;
7. neutral wording that describes the implementation without speculating about intent.

See [`docs/evidence-standard.md`](docs/evidence-standard.md) and [`TAXONOMY.md`](TAXONOMY.md).

## Repository map

```text
cases/                  One reviewed Markdown record per case
corpus/sources.csv      Frozen corpus and screening decisions
data/cases.csv          Machine-readable case index
docs/                   Methodology, evidence rules, and roadmap
schemas/                JSON Schema for structured case records
scripts/                Validation and summary tools
talk/                    Lightning-talk outline
tests/                   Validator tests
```

## Validate the artifact

Python 3.10 or newer is enough; the validator has no third-party runtime dependencies.

```bash
python scripts/validate_cases.py
python -m unittest discover -s tests -v
```

## Add a candidate

1. Add the exact source and revision to `corpus/sources.csv`.
2. Copy [`cases/CASE_TEMPLATE.md`](cases/CASE_TEMPLATE.md) to a new case file.
3. Add a corresponding row to `data/cases.csv`.
4. Include archived evidence only when its license permits redistribution; otherwise record a stable URL, revision, file path, and line range.
5. Run the validator and open a pull request using the review checklist.

Candidates are not automatically findings. A suspicious pattern such as `fit_transform` before `train_test_split` still needs task-specific verification.

## Outputs

- Versioned GitHub dataset and documentation
- Zenodo archive and DOI after the first reviewed release
- Summary analysis after a sufficient verified sample exists
- Conference lightning-talk submission based on reviewed findings
- A future benchmark for agents that detect and explain leakage

## Responsible reporting

This project studies code and evaluation design. It does not label authors as careless or deceptive. Findings are confidence-scored, corrections are welcome, and disputed cases remain visible with their status and rationale.

## Citation and license

Citation metadata is in [`CITATION.cff`](CITATION.cff). Dataset and written case annotations are licensed under [CC BY 4.0](LICENSE-DATA); repository code is licensed under the [MIT License](LICENSE-CODE). Source projects retain their own copyrights and licenses.

