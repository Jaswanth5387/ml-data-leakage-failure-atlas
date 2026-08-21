---
case_id: MLA-010
title: Cardiovascular classifier scales the full dataset before splitting
status: verified
confidence: confirmed
primary_mechanism: preprocessing
subtype: scaling_before_split
source_type: github
source_url: https://github.com/ChapaMchivi/Cardiovascular-Disease-Dataset/blob/15e612a346cafe467ccd75959bea1b6eaac51d27/README.md
source_revision: 15e612a346cafe467ccd75959bea1b6eaac51d27
reproduction_status: static_verified
impact_basis: inferred
---

# MLA-010 — Cardiovascular classifier scales the full dataset before splitting

## Source and task

- Project: `ChapaMchivi/Cardiovascular-Disease-Dataset`
- Artifact: `README.md`, commit `15e612a`, lines 313–317
- Task: classify the presence of cardiovascular disease
- Intended boundary: holdout rows must not affect scaling parameters learned for training
- Source license: not stated in the repository

## Evidence

The [pinned project report](https://github.com/ChapaMchivi/Cardiovascular-Disease-Dataset/blob/15e612a346cafe467ccd75959bea1b6eaac51d27/README.md#L313-L317) constructs a `StandardScaler`, runs `X_scaled = scaler.fit_transform(X)` on all features, and then calls `train_test_split(X_scaled, y, ...)`.

## Information flow

Means and variances from rows later assigned to the test partition affect the representation on which the classifier is trained.

## Why this is leakage

The test set should simulate unseen data. Using it to fit a transformer before training weakens that evaluation boundary.

## Impact

`inferred`. No corrected rerun has measured the size or direction of the metric change.

## Correction

Split raw features first and combine `StandardScaler` with the classifier in a pipeline. Fit that pipeline on training data and use its unchanged transform for the test data.

## Reproduction

- Outcome: static code and execution-order verification
- Date checked: 2026-08-21
- Controlled rerun: not yet performed

## Review

- Evidence status: one reviewer; independent review pending
- Open question: reproduce the reported classifiers with train-only scaling
