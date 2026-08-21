---
case_id: MLA-008
title: DualGCN uses its test partition for early stopping and checkpoint selection
status: verified
confidence: confirmed
primary_mechanism: evaluation
subtype: test_set_early_stopping
source_type: github
source_url: https://github.com/horsedayday/DualGCN/blob/91e42e9000900f150efe5eb99945d26ec3661ca6/code/DualGCN.py
source_revision: 91e42e9000900f150efe5eb99945d26ec3661ca6
reproduction_status: static_verified
impact_basis: inferred
---

# MLA-008 — DualGCN uses its test partition for early stopping and checkpoint selection

## Source and task

- Project: `horsedayday/DualGCN`
- Artifact: `code/DualGCN.py`, commit `91e42e9`, lines 236–257 and 309–340
- Task: predict cancer drug response from cell-line and drug inputs
- Intended boundary: the test partition must remain untouched until training and checkpoint selection are complete
- Source license: not stated in the repository

## Evidence

In the [pinned training script](https://github.com/horsedayday/DualGCN/blob/91e42e9000900f150efe5eb99945d26ec3661ca6/code/DualGCN.py#L236-L257), the callback computes Pearson correlation on supplied validation labels, keeps the best weights, and stops training after the patience limit. Lines 309–340 build `test_data = [X_test, Y_test]` and pass it as `validation_data` to `ModelTraining`; the same test data is then used by `ModelEvaluate`.

## Information flow

Test labels determine when training stops and which weights are retained. The final evaluation therefore reuses a partition that already influenced the selected model.

## Why this is leakage

A test set is reserved for final evaluation. Supplying it to an early-stopping callback and checkpoint selector adapts the model to test outcomes.

## Impact

`inferred`. The reported test performance may be optimistic, but this record does not claim a measured inflation amount.

## Correction

Create a validation partition from the training data for early stopping and checkpoint selection. Evaluate the frozen model once on the untouched test partition.

## Reproduction

- Outcome: static data-flow, callback, and call-site verification
- Date checked: 2026-08-21
- Controlled rerun: not yet performed

## Review

- Evidence status: one reviewer; independent review pending
- Open question: rerun with training-derived validation data and quantify the difference
