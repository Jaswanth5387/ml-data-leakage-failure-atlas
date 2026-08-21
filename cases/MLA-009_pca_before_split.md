---
case_id: MLA-009
title: Capstone project fits scaling and PCA before its holdout split
status: verified
confidence: confirmed
primary_mechanism: preprocessing
subtype: dimensionality_reduction_before_split
source_type: github
source_url: https://github.com/Alshehri-Ahmad/Udacity-Machine-Learning-Nanodegree-Capstone/blob/8365f9f2727cdb5e537a492081955e547b75d9a6/Code.ipynb
source_revision: 8365f9f2727cdb5e537a492081955e547b75d9a6
reproduction_status: static_verified
impact_basis: inferred
---

# MLA-009 — Capstone project fits scaling and PCA before its holdout split

## Source and task

- Project: `Alshehri-Ahmad/Udacity-Machine-Learning-Nanodegree-Capstone`
- Artifact: `Code.ipynb`, commit `8365f9f`, code cells 9, 13, 15, 19, and 23
- Task: classify music tracks as rock or hip-hop using audio features
- Intended boundary: holdout rows and validation folds must not influence fitted scaling or PCA components
- Source license: not stated in the repository

## Evidence

The [pinned notebook](https://github.com/Alshehri-Ahmad/Udacity-Machine-Learning-Nanodegree-Capstone/blob/8365f9f2727cdb5e537a492081955e547b75d9a6/Code.ipynb) fits `StandardScaler` on the complete feature matrix in cell 9, fits PCA and creates `pca_projection` in cell 13, and only creates the holdout with `train_test_split(pca_projection, labels, ...)` in cell 15. Cell 19 repeats the full-data scaler-and-PCA fit before splitting, and cell 23 evaluates estimators with `cross_val_score` on the already fitted projection.

## Information flow

Evaluation rows affect the scaling statistics and the principal directions used to represent training rows. The same global projection also lets every cross-validation fold influence the representation used by the other folds.

## Why this is leakage

PCA and scaling are data-dependent transformations. Both must be fitted inside each training partition rather than on data later used for evaluation.

## Impact

`inferred`. The validation estimates may be optimistic, but no numeric effect is claimed.

## Correction

Place `StandardScaler`, `PCA`, and the classifier in one pipeline. Pass raw features to the holdout or cross-validation procedure so the pipeline is refitted separately inside each training fold.

## Reproduction

- Outcome: static code and execution-order verification
- Date checked: 2026-08-21
- Controlled rerun: not yet performed

## Review

- Evidence status: one reviewer; independent review pending
- Open question: compare model selection and holdout scores under fold-local PCA
