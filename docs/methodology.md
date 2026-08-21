# Methodology

## 1. Current scope

The two completed tranches form a targeted GitHub discovery corpus. It contains 15 repositories frozen at exact commits on 2026-08-21 and spans tabular regression, imbalanced classification, fraud detection, loan default, demand forecasting, Titanic survival, medical imaging, cardiovascular classification, and multi-omics drug response.

Thirteen sources produced verified cases. Two sources were retained as negative screening results after closer inspection disproved the suspected information path or showed it was a no-op. The unit of screening is a specific file at a commit, not a moving default branch.

This is not a prevalence sample. Candidate-search signatures deliberately over-sample likely failures. Counts describe this atlas tranche only.

## 2. Corpus freeze

Store repository/file identity, commit SHA, permalink, collection timestamp, license status, screening state, duplicate group, and notes in `corpus/sources.csv`.

The frozen manifest controls inclusion. Later repository changes do not alter a released tranche. A new commit is a new screening unit when the relevant pipeline changes.

### Discovery signatures for tranches 1 and 2

- `fit_transform` or full-matrix scaling before `train_test_split`
- `SMOTE.fit_resample` before `train_test_split`
- default shuffled `train_test_split` in a forecasting task
- Titanic `boat` or `body` fields used to predict survival
- duplicate or near-duplicate images discussed across train/test boundaries
- full-data imputation, feature selection, or PCA before holdout splitting or cross-validation
- variables named as test data supplied to training callbacks or evaluated repeatedly for best-epoch selection

Search results were manually checked against execution order and task semantics. A matching string did not determine the verdict.

### Planned Kaggle tranche

The next corpus freeze will sample up to 100 public notebook versions from each of five named competition ecosystems: Home Credit Default Risk, IEEE-CIS Fraud Detection, M5 Forecasting — Accuracy, Store Sales — Time Series Forecasting, and Histopathologic Cancer Detection. The exact slugs and versions must be exported before screening.

## 3. Inclusion criteria

- Public source is inspectable at an immutable commit, notebook version, DOI, or archive.
- The artifact trains, evaluates, or directly audits an ML system or source corpus.
- The prediction target and intended evaluation boundary can be established.
- Enough code and data semantics are available to trace the suspected information path.

## 4. Exclusion criteria

- Hypothetical tutorials or prose-only discussions with no traced implementation or dataset audit.
- Forks that reproduce the same leaking implementation without a meaningful change; record them as related sources rather than new cases.
- Inaccessible versions, missing essential data, or licenses that prohibit the needed inspection.
- Suspicious code patterns that do not cross the task's actual evaluation boundary.

## 5. Candidate discovery

Search code and execution order for indicators such as:

- target encoding, grouped target statistics, and post-outcome columns;
- `shift`, rolling windows, global aggregates, random splits in time-indexed tasks;
- fitting scalers, imputers, selectors, PCA, encoders, or resampling before a split;
- hashes, IDs, groups, or perceptual similarity indicating overlap across folds.
- test-set metrics or labels used for early stopping, checkpoint selection, threshold selection, or tuning.

These indicators prioritize review. They do not determine the verdict.

## 6. Verification

Two checks are required for `confirmed` status:

1. **Boundary check:** document what information should be unavailable to the model at prediction time or during evaluation.
2. **Flow check:** trace how that unavailable information reaches training, feature construction, model selection, or evaluation.

Whenever feasible, independently rerun the original pipeline and a minimally corrected variant. Keep random seeds, folds, metrics, and environment fixed. Report all rerun failures.

## 7. Review and disagreement

One researcher drafts a case and another reviewer checks the source, boundary, mechanism, confidence, and wording. Until that review happens, the case status is `candidate` or `under_review`.

Source authors may open a correction issue. Substantive corrections are versioned; records are not silently removed.

## 8. Counting rules

- Headline total: cases with status `verified` and confidence `confirmed` or `probable`.
- One underlying information path counts as one case even if it appears in several cells.
- Independent leakage mechanisms in one notebook may be separate cases when each has distinct evidence and correction.
- Cloned or copied implementations are grouped to avoid inflating prevalence.

## 9. Limitations

The corpus is not representative of all ML practice. Public notebooks favor successful, visible work and may differ from production systems. Missing environments can prevent impact measurement. Finding leakage in a public artifact does not establish that the same issue existed in any private or production pipeline.
