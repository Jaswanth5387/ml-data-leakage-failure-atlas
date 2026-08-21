---
case_id: MLA-006
title: Titanic example predicts survival with lifeboat assignment
status: verified
confidence: confirmed
primary_mechanism: target
subtype: post_outcome_feature
source_type: github
source_url: https://github.com/vertica/VerticaPy/blob/05b2882a2a9c8389c4778c84c57077a503e8597a/README.md
source_revision: 05b2882a2a9c8389c4778c84c57077a503e8597a
reproduction_status: static_verified
impact_basis: inferred
---

# MLA-006 — Titanic example predicts survival with lifeboat assignment

## Source and task

- Project: `vertica/VerticaPy`
- Artifact: `README.md`, commit `05b2882`, lines 530–553
- Task: cross-validate a random-forest classifier for Titanic passenger survival
- Intended boundary: predictors must be knowable before the survival outcome
- Source license: Apache-2.0

## Evidence

The [pinned quickstart](https://github.com/vertica/VerticaPy/blob/05b2882a2a9c8389c4778c84c57077a503e8597a/README.md#L530-L553) preprocesses `boat` and includes it in the predictor list for `survived` during cross-validation and model fitting.

The dataset definition identifies `boat` as lifeboat information. A [published data dictionary](https://www.kaggle.com/datasets/sakshisatre/titanic-dataset) further states that this field contains the rescue lifeboat for survivors.

## Information flow

Lifeboat assignment is recorded during or after the disaster and is closely tied to survival. It is unavailable at any meaningful pre-outcome prediction point, yet it enters every cross-validation fold as a feature.

## Why this is leakage

The model is given a post-outcome proxy for the label. Cross-validation cannot repair a feature whose availability violates the prediction-time boundary.

## Impact

`inferred`. The feature should strongly inflate apparent discrimination, but this atlas does not claim a numeric increase until a controlled rerun removes `boat`.

## Correction

Exclude `boat`, `body`, and any other fields recorded after the sinking outcome. Define a prediction timestamp and permit only variables available by that time.

## Reproduction

- Outcome: static feature-list and data-semantics verification
- Date checked: 2026-08-21
- Controlled rerun: not yet performed

## Review

- Evidence status: one reviewer; independent review pending
- Open question: rerun identical folds with and without `boat` and report the paired score difference
