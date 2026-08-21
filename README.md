# ML Data Leakage Failure Atlas

An evidence-first catalog of data leakage found in real, publicly accessible machine-learning projects.

This repository is a research artifact, not a collection of textbook examples. Every accepted case must point to a stable public source, identify the exact leaking code or data operation, explain the violated evaluation boundary, and record how the finding was checked.

> **Project status:** first research tranche. There are currently **7 verified, commit-pinned cases**. All seven are statically verified and have `inferred`, not measured, impact. Controlled reruns are the next stage.

## Research question

How does data leakage appear in public ML work, how strong is the available evidence, and what changes when the leaking pipeline is corrected?

## Current frozen corpus

The first completed screening tranche contains eight public GitHub repositories frozen at exact commits on 2026-08-21. Seven contain verified findings; one screened candidate did not use the suspected leaking field and remains in the manifest as a negative screening result.

This tranche was selected with fixed candidate-discovery signatures for preprocessing before splitting, resampling before splitting, random time-series splitting, post-outcome Titanic fields, and duplicate medical images. It is a targeted discovery corpus, not a random sample, so its mechanism counts must not be presented as prevalence estimates.

The exact source and revision list lives in [`corpus/sources.csv`](corpus/sources.csv). A separately frozen Kaggle tranche across the five competition ecosystems originally proposed is still planned. Selection and counting rules are in [`docs/methodology.md`](docs/methodology.md).

## Verified cases

| Case | Mechanism | Real source | Evidence status |
|---|---|---|---|
| [MLA-001](cases/MLA-001_flood_scaling_before_split.md) | Scaling before split | Kaggle flood-prediction project | Static, impact inferred |
| [MLA-002](cases/MLA-002_academic_success_smote_before_split.md) | SMOTE before split | Academic-success classification project | Static, impact inferred |
| [MLA-003](cases/MLA-003_fraud_scaling_before_split.md) | Scaling before split | Credit-card fraud project | Static, impact inferred |
| [MLA-004](cases/MLA-004_loan_default_scaling_before_split.md) | Scaling before split | Loan-default prediction project | Static, impact inferred |
| [MLA-005](cases/MLA-005_store_demand_random_time_split.md) | Random temporal split | Store-item demand forecast | Static, impact inferred |
| [MLA-006](cases/MLA-006_titanic_lifeboat_target_leakage.md) | Post-outcome feature | VerticaPy Titanic quickstart | Static, impact inferred |
| [MLA-007](cases/MLA-007_covid_xray_duplicate_contamination.md) | Near-duplicate contamination | COVID chest X-ray project | Static, impact inferred |

Current mechanism count: preprocessing 4, temporal 1, target 1, contamination 1.

## What qualifies as a case

A case must include:

1. a real, citable public source and immutable revision identifier;
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

Candidates are not automatically findings. For example, `shantnu/Titanic-Machine-Learning` appeared in a search because its dataset contains a `boat` column, but the pinned model uses only class, age, and sex. It is retained as `no_leakage_detected` rather than being padded into the case count.

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
