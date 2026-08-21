# ML Data Leakage Failure Atlas

An evidence-first catalog of data leakage found in real, publicly accessible machine-learning projects.

This repository is a research artifact, not a collection of textbook examples. Every accepted case must point to a stable public source, identify the exact leaking code or data operation, explain the violated evaluation boundary, and record how the finding was checked.

> **Version 0.1.0 scope:** three targeted research tranches with **18 verified cases at immutable revisions**. Five have controlled impact comparisons reported by their primary sources; the atlas has not yet independently rerun them.

## Research question

How does data leakage appear in public ML work, how strong is the available evidence, and what changes when the leaking pipeline is corrected?

## Current frozen corpus

The completed screening corpus contains 20 immutable sources: 15 public GitHub artifacts and five primary research papers. Eighteen contain verified findings; two GitHub candidates failed the evidence test and remain in the manifest as negative screening results.

The tranches were selected with fixed candidate-discovery signatures for preprocessing before splitting, resampling before splitting, random time-series splitting, post-outcome Titanic fields, duplicate medical images, and use of a test partition during training or model selection. This is a targeted discovery corpus, not a random sample, so its mechanism counts must not be presented as prevalence estimates.

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
| [MLA-008](cases/MLA-008_dualgcn_test_set_early_stopping.md) | Test-set early stopping | DualGCN | Static, impact inferred |
| [MLA-009](cases/MLA-009_pca_before_split.md) | Scaling and PCA before split | ML capstone project | Static, impact inferred |
| [MLA-010](cases/MLA-010_cardiovascular_scaling_before_split.md) | Scaling before split | Cardiovascular-disease project | Static, impact inferred |
| [MLA-011](cases/MLA-011_deepcdr_test_set_early_stopping.md) | Test-set early stopping | DeepCDR | Static, impact inferred |
| [MLA-012](cases/MLA-012_drugcell_test_set_model_selection.md) | Test-set model selection | DrugCell | Static, impact inferred |
| [MLA-013](cases/MLA-013_moli_feature_selection_before_cv.md) | Feature selection before CV | MOLI | Static, impact inferred |
| [MLA-014](cases/MLA-014_stroke_missingness_target_proxy.md) | Target-dependent missingness | Stroke-type study | Static, source impact measured |
| [MLA-015](cases/MLA-015_panel_forecasting_temporal_leakage.md) | Future periods and contemporaneous predictors | US county panel study | Static, source impact measured |
| [MLA-016](cases/MLA-016_oct_subject_overlap.md) | Subject/volume overlap | OCT classification study | Static, source impact measured |
| [MLA-017](cases/MLA-017_connectome_feature_selection_leakage.md) | Supervised feature selection before CV | Connectome study | Static, source impact measured |
| [MLA-018](cases/MLA-018_eeg_augmentation_overlap.md) | Augmentation and patient overlap | PTSD EEG study | Static, source impact measured |

Current mechanism count: preprocessing 8, evaluation 3, contamination 3, temporal 2, target 2.

Impact evidence: 5 `source_measured` and 13 `inferred`. `source_measured` means the primary source published a controlled leaky-versus-corrected comparison; it does not mean this atlas independently reproduced the experiment.

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
python scripts/check_release.py 0.1.0
```

## Add a candidate

1. Add the exact source and revision to `corpus/sources.csv`.
2. Copy [`cases/CASE_TEMPLATE.md`](cases/CASE_TEMPLATE.md) to a new case file.
3. Add a corresponding row to `data/cases.csv`.
4. Include archived evidence only when its license permits redistribution; otherwise record a stable URL, revision, file path, and line range.
5. Run the validator and open a pull request using the review checklist.

Candidates are not automatically findings. For example, `shantnu/Titanic-Machine-Learning` appeared in a search because its dataset contains a `boat` column, but the pinned model uses only class, age, and sex. A second candidate fitted an imputer before splitting, but its inspected feature matrix reported zero missing values, so the suspected information path was a no-op. Both are retained as `no_leakage_detected` rather than being padded into the case count.

## Outputs

- Versioned GitHub dataset and documentation
- Zenodo archive and DOI after the first reviewed release
- Summary analysis after a sufficient verified sample exists
- Conference lightning-talk submission based on reviewed findings
- A future benchmark for agents that detect and explain leakage

## Responsible reporting

This project studies code and evaluation design. It does not label authors as careless or deceptive. Findings are confidence-scored, corrections are welcome, and disputed cases remain visible with their status and rationale.

## Citation and license

Citation metadata is in [`CITATION.cff`](CITATION.cff), and Zenodo deposit metadata is in [`.zenodo.json`](.zenodo.json). Dataset and written case annotations are licensed under [CC BY 4.0](LICENSE-DATA); repository code is licensed under the [MIT License](LICENSE-CODE). Source projects retain their own copyrights and licenses.

The DOI will be added after Zenodo archives the `v0.1.0` GitHub release. See the [release checklist](docs/release-checklist.md) for the exact publication sequence.
Prepared release notes are in [`docs/release-notes-v0.1.0.md`](docs/release-notes-v0.1.0.md).
