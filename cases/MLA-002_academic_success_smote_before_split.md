---
case_id: MLA-002
title: Academic-success project applies SMOTE before the holdout split
status: verified
confidence: confirmed
primary_mechanism: preprocessing
subtype: resampling_before_split
source_type: github
source_url: https://github.com/Osama-Abo-Bakr/ML-Classification-with-an-Academic-Success-Dataset/blob/0916d5c99870e2af4388bfb9936ee8fb6b6685bc/README.md
source_revision: 0916d5c99870e2af4388bfb9936ee8fb6b6685bc
reproduction_status: static_verified
impact_basis: inferred
---

# MLA-002 — Academic-success project applies SMOTE before the holdout split

## Source and task

- Project: `Osama-Abo-Bakr/ML-Classification-with-an-Academic-Success-Dataset`
- Artifact: `README.md`, commit `0916d5c`, lines 131–138
- Task: classify student academic outcomes
- Intended boundary: class balancing and scaling must be learned only from training rows
- Source license: not stated in the repository

## Evidence

The [pinned workflow](https://github.com/Osama-Abo-Bakr/ML-Classification-with-an-Academic-Success-Dataset/blob/0916d5c99870e2af4388bfb9936ee8fb6b6685bc/README.md#L131-L138) calls `SMOTE.fit_resample(X, Y)`, scales the resampled matrix, and only then calls `train_test_split`.

## Information flow

1. SMOTE constructs synthetic samples using neighbors from the full labeled dataset.
2. The later split can place related original and synthetic samples on opposite sides of the holdout boundary.
3. The holdout is also artificially rebalanced instead of retaining the natural outcome distribution.
4. `MinMaxScaler` is fitted before the split as a second preprocessing leak.

## Why this is leakage

Imbalanced-learn documents [resampling the entire dataset before splitting](https://imbalanced-learn.org/stable/common_pitfalls.html#data-leakage) as a common leakage pitfall because test-sample information can influence generated samples and evaluation distribution.

## Impact

`inferred`. The reported test scores can be optimistic and are measured on a synthetic class balance. No controlled rerun has quantified the difference.

## Correction

Create the holdout from the original data first. Fit SMOTE and `MinMaxScaler` only inside an imbalanced-learn pipeline applied to each training fold; evaluate on untouched, naturally distributed rows.

## Reproduction

- Outcome: static code and execution-order verification
- Date checked: 2026-08-21
- Controlled rerun: not yet performed

## Review

- Evidence status: one reviewer; independent review pending
- Open question: compare both discrimination and calibration on the original holdout distribution
