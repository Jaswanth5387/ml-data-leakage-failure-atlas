---
case_id: MLA-003
title: Fraud project fits StandardScaler before the stratified split
status: verified
confidence: confirmed
primary_mechanism: preprocessing
subtype: scaling_before_split
source_type: github
source_url: https://github.com/DrushtiV/Credit-Card-Fraud-Detection-/blob/b58a38c4329f1ecf8dd07727114e5508d48f1696/README.md
source_revision: b58a38c4329f1ecf8dd07727114e5508d48f1696
reproduction_status: static_verified
impact_basis: inferred
---

# MLA-003 — Fraud project fits StandardScaler before the stratified split

## Source and task

- Project: `DrushtiV/Credit-Card-Fraud-Detection-`
- Artifact: `README.md`, commit `b58a38c`, lines 124–142
- Task: classify credit-card transactions as fraud or legitimate
- Intended boundary: the stratified test set must not affect fitted scaling
- Source license: not stated in the repository

## Evidence

In the [pinned preprocessing section](https://github.com/DrushtiV/Credit-Card-Fraud-Detection-/blob/b58a38c4329f1ecf8dd07727114e5508d48f1696/README.md#L124-L142), `scaler.fit_transform(X)` precedes `train_test_split(X_scaled, ...)`.

The accompanying prose says the scaler is fitted only on training data, but the displayed code fits it on the full feature matrix. This record follows the executable order shown by the code and flags the documentation inconsistency rather than assuming which one the author intended.

## Information flow

Full-dataset means and standard deviations include the eventual test rows. Those learned statistics are embedded in both the training and test representations before evaluation.

## Why this is leakage

Scikit-learn explicitly lists `StandardScaler` among transforms at risk when fitted before splitting and recommends a [pipeline](https://scikit-learn.org/stable/modules/compose.html#pipeline-safety) to keep fold statistics isolated.

## Impact

`inferred`. Directionally, independence is weakened; the metric change is unknown. For this dataset, most V-features are already PCA transformed, so the effect may be small and must not be exaggerated.

## Correction

Split the raw feature frame first, then fit the scaler on `X_train` and call `transform` on `X_test`. Keep SMOTE restricted to the training partition as the project already does.

## Reproduction

- Outcome: static code and prose consistency check
- Date checked: 2026-08-21
- Controlled rerun: not yet performed

## Review

- Evidence status: one reviewer; independent review pending
- Open question: determine whether the repository's runnable script matches the README code or its prose
