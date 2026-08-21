---
case_id: MLA-011
title: DeepCDR uses its test partition for training-time model selection
status: verified
confidence: confirmed
primary_mechanism: evaluation
subtype: test_set_early_stopping
source_type: github
source_url: https://github.com/kimmo1019/DeepCDR/blob/4dc5a901d580511335b9a54ffce9fb188f9f068d/prog/run_DeepCDR.py
source_revision: 4dc5a901d580511335b9a54ffce9fb188f9f068d
reproduction_status: static_verified
impact_basis: inferred
---

# MLA-011 — DeepCDR uses its test partition for training-time model selection

## Source and task

- Project: `kimmo1019/DeepCDR`
- Artifact: `prog/run_DeepCDR.py`, commit `4dc5a90`, lines 201–245 and 278–281
- Task: predict cancer drug response from multi-omics and drug-graph inputs
- Intended boundary: the test partition must remain untouched until model and epoch selection are complete
- Source license: not stated in the repository

## Evidence

In the [pinned training script](https://github.com/kimmo1019/DeepCDR/blob/4dc5a901d580511335b9a54ffce9fb188f9f068d/prog/run_DeepCDR.py#L201-L245), `MyCallback` receives validation data and evaluates it during training. Lines 278–281 assemble that `validation_data` from variables named `*_test` and `Y_test`, then pass it into `ModelTraining`.

## Information flow

Test outcomes are evaluated during fitting and influence the callback's training-time decisions. The final reported test performance is therefore no longer based on a partition untouched by model selection.

## Why this is leakage

A test set is reserved for final evaluation. Reusing it as validation data for early stopping or checkpoint decisions adapts the selected model to the test labels.

## Impact

`inferred`. The selected result may be optimistic; this record does not claim a measured inflation amount.

## Correction

Create a validation partition from training data for callbacks and checkpoint selection. Evaluate the frozen model once on the untouched test partition, or use nested resampling when all observations are needed for tuning.

## Reproduction

- Outcome: static data-flow and call-site verification
- Date checked: 2026-08-21
- Controlled rerun: not yet performed

## Review

- Evidence status: one reviewer; independent review pending
- Open question: rerun with a training-derived validation set and quantify the difference
