---
case_id: MLA-013
title: MOLI fits variance-based feature selection before cross-validation
status: verified
confidence: confirmed
primary_mechanism: preprocessing
subtype: feature_selection_before_split
source_type: github
source_url: https://github.com/hosseinshn/MOLI/blob/c83d6d4c7e042ff4da7c7e3df0a7c8d030d37b8b/Cross%20validation/MOLI%20Complete/Erlotinib_cvSoftTripletClassifierNetv16_Script.py
source_revision: c83d6d4c7e042ff4da7c7e3df0a7c8d030d37b8b
reproduction_status: static_verified
impact_basis: inferred
---

# MLA-013 — MOLI fits variance-based feature selection before cross-validation

## Source and task

- Project: `hosseinshn/MOLI`
- Artifact: `Cross validation/MOLI Complete/Erlotinib_cvSoftTripletClassifierNetv16_Script.py`, commit `c83d6d4`, lines 62–64 and 135
- Task: predict response to erlotinib using multi-omics inputs
- Intended boundary: each validation fold must not influence features selected for its training fold
- Source license: not stated in the repository

## Evidence

The [pinned script](https://github.com/hosseinshn/MOLI/blob/c83d6d4c7e042ff4da7c7e3df0a7c8d030d37b8b/Cross%20validation/MOLI%20Complete/Erlotinib_cvSoftTripletClassifierNetv16_Script.py#L62-L64) fits `VarianceThreshold(0.05)` to the full `GDSCE` expression matrix and applies the selected columns. Cross-validation begins later at line 135 with `skf.split(...)`.

## Information flow

Every observation, including each future validation fold, contributes to the variance calculation that decides which expression features are available to the model.

## Why this is leakage

Even unsupervised feature selection learns from the data distribution. Fitting it globally before cross-validation lets validation-fold information shape the training representation.

## Impact

`inferred`. No controlled fold-local rerun is available in this record.

## Correction

Fit `VarianceThreshold` independently inside each training fold and apply the learned column mask to that fold's validation data. A pipeline or fold-local preprocessing function can enforce this order.

## Reproduction

- Outcome: static code and execution-order verification
- Date checked: 2026-08-21
- Controlled rerun: not yet performed

## Review

- Evidence status: one reviewer; independent review pending
- Open question: measure whether fold-local selection changes retained genes or validation performance
