---
case_id: MLA-004
title: Loan-default project scales before creating its validation set
status: verified
confidence: confirmed
primary_mechanism: preprocessing
subtype: scaling_before_split
source_type: github
source_url: https://github.com/OleksiyM/Loan-Default-Predictor/blob/f795bddfb37d1bfb45bc12c0dc06fe4a6a0905e0/LoanDefaultPrediction_v4.ipynb
source_revision: f795bddfb37d1bfb45bc12c0dc06fe4a6a0905e0
reproduction_status: static_verified
impact_basis: inferred
---

# MLA-004 — Loan-default project scales before creating its validation set

## Source and task

- Project: `OleksiyM/Loan-Default-Predictor`
- Artifact: `LoanDefaultPrediction_v4.ipynb`, commit `f795bdd`, code cell 19
- Task: predict the `Default` outcome for loan applications
- Intended boundary: validation rows must not affect scaling or hyperparameter selection
- Source license: not stated in the repository

## Evidence

The [pinned notebook](https://github.com/OleksiyM/Loan-Default-Predictor/blob/f795bddfb37d1bfb45bc12c0dc06fe4a6a0905e0/LoanDefaultPrediction_v4.ipynb) creates `X_scaled = scaler.fit_transform(X)` in cell 19 and then passes `X_scaled` to a stratified `train_test_split`.

The resulting validation set is used to report AUC after `RandomizedSearchCV` fits models on the training portion.

## Information flow

The scaler learns from every labeled row, including the rows later used for validation. Their distribution therefore affects the model inputs used during fitting and AUC selection.

## Why this is leakage

The validation set should represent unseen data. Fitting a data-dependent transformer on it before model selection violates that boundary.

## Impact

`inferred`. The validation AUC may be optimistic, but no numeric effect is claimed.

## Correction

Split first and wrap `StandardScaler` plus the classifier in a pipeline passed to `RandomizedSearchCV`. Fit the final selected pipeline on all labeled training data only after validation decisions are frozen.

## Reproduction

- Outcome: static code and execution-order verification
- Date checked: 2026-08-21
- Controlled rerun: not yet performed

## Review

- Evidence status: one reviewer; independent review pending
- Open question: measure whether corrected scaling changes the selected parameters or validation AUC
