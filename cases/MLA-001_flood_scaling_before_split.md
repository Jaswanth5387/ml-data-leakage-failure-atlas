---
case_id: MLA-001
title: Flood predictor scales the holdout before splitting
status: verified
confidence: confirmed
primary_mechanism: preprocessing
subtype: scaling_before_split
source_type: github
source_url: https://github.com/Leohoji/kaggle-competition-flood-prediction-project/blob/f23fdc281550107525e955df817a21ab6451166a/flood_prediction.ipynb
source_revision: f23fdc281550107525e955df817a21ab6451166a
reproduction_status: static_verified
impact_basis: inferred
---

# MLA-001 — Flood predictor scales the holdout before splitting

## Source and task

- Project: `Leohoji/kaggle-competition-flood-prediction-project`
- Artifact: `flood_prediction.ipynb`, commit `f23fdc2`, code cell 33
- Task: predict `FloodProbability` in Kaggle's Regression with a Flood Prediction Dataset competition
- Intended boundary: the local holdout must not influence fitted preprocessing
- Source license: not stated in the repository

## Evidence

[The pinned notebook](https://github.com/Leohoji/kaggle-competition-flood-prediction-project/blob/f23fdc281550107525e955df817a21ab6451166a/flood_prediction.ipynb) fits `StandardScaler` on all of `X` in cell 33 and then passes the scaled matrix to `train_test_split`.

## Information flow

1. `StandardScaler.fit_transform(X)` computes means and standard deviations from every row.
2. `train_test_split` subsequently assigns some of those rows to the local holdout.
3. Holdout statistics have therefore already influenced the representation used to train and score the model.

## Why this is leakage

Scikit-learn's [data-leakage guidance](https://scikit-learn.org/stable/common_pitfalls.html#data-leakage) says to split before preprocessing and never include test data in `fit` or `fit_transform`. The notebook reverses that order.

## Impact

`inferred`. The holdout is no longer fully independent, so its score may be optimistic. The magnitude has not been measured.

## Correction

Split raw `X` first. Fit the scaler on `X_train`, transform both partitions with that fitted scaler, or place `StandardScaler` and the estimator in a `Pipeline`.

## Reproduction

- Outcome: static code and execution-order verification
- Date checked: 2026-08-21
- Controlled leaky-versus-corrected rerun: not yet performed

## Review

- Evidence status: one reviewer; independent review pending
- Open question: quantify the holdout-score change under identical seeds
