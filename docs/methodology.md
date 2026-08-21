# Methodology

## 1. Scope

The pilot study uses a bounded Kaggle corpus spanning tabular classification, fraud detection, forecasting, and image classification. The five competition ecosystems are named in the root README.

The unit of screening is a specific notebook version. Updated notebooks are separate versions when the relevant pipeline changed.

## 2. Corpus freeze

For each competition, collect up to 100 public notebooks ordered by Kaggle's public vote ranking on the collection date. Store the notebook slug, version number, URL, collection timestamp, license/access status, and screening state in `corpus/sources.csv`.

The frozen manifest controls inclusion. Later ranking changes do not alter a released corpus. If fewer than 100 notebooks are accessible, record all accessible notebooks and the reason the target was not reached.

## 3. Inclusion criteria

- Public source is inspectable at a stable notebook version or archived revision.
- The notebook trains or evaluates an ML system on the named competition data.
- The prediction target and intended evaluation boundary can be established.
- Enough code and data semantics are available to trace the suspected information path.

## 4. Exclusion criteria

- Tutorials or prose-only discussions with no executed project pipeline.
- Forks that reproduce the same leaking implementation without a meaningful change; record them as related sources rather than new cases.
- Inaccessible versions, missing essential data, or licenses that prohibit the needed inspection.
- Suspicious code patterns that do not cross the task's actual evaluation boundary.

## 5. Candidate discovery

Search code and execution order for indicators such as:

- target encoding, grouped target statistics, and post-outcome columns;
- `shift`, rolling windows, global aggregates, random splits in time-indexed tasks;
- fitting scalers, imputers, selectors, PCA, encoders, or resampling before a split;
- hashes, IDs, groups, or perceptual similarity indicating overlap across folds.

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

