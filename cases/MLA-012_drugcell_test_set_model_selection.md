---
case_id: MLA-012
title: DrugCell selects its best epoch from test-set correlation
status: verified
confidence: confirmed
primary_mechanism: evaluation
subtype: test_set_model_selection
source_type: github
source_url: https://github.com/idekerlab/DrugCell/blob/c507e1d821fac0201e42f831a1d772e7ef42b00e/code/train_drugcell.py
source_revision: c507e1d821fac0201e42f831a1d772e7ef42b00e
reproduction_status: static_verified
impact_basis: inferred
---

# MLA-012 — DrugCell selects its best epoch from test-set correlation

## Source and task

- Project: `idekerlab/DrugCell`
- Artifact: `code/train_drugcell.py`, commit `c507e1d`, lines 67 and 122–146
- Task: predict drug response from genotype and drug structure
- Intended boundary: the test partition must not choose an epoch or checkpoint
- Source license: not stated in the repository

## Evidence

The [pinned training script](https://github.com/idekerlab/DrugCell/blob/c507e1d821fac0201e42f831a1d772e7ef42b00e/code/train_drugcell.py#L122-L146) evaluates `test_loader` at every epoch, computes `test_corr`, and updates `max_corr` and `best_model` when that test correlation improves. The script then reports the best-performing epoch.

## Information flow

Repeated access to test labels determines which epoch is identified as best. The chosen model is therefore adapted to noise and idiosyncrasies in the test partition.

## Why this is leakage

Test data can support one final estimate after model selection. Using its metric to select among epochs turns the test set into a validation set.

## Impact

`inferred`. Repeated selection on test correlation can bias the selected score upward, but no magnitude is claimed here.

## Correction

Choose the best epoch with a validation set drawn from training data. Lock that epoch-selection rule before a single evaluation on the untouched test set.

## Reproduction

- Outcome: static data-flow and selection-logic verification
- Date checked: 2026-08-21
- Controlled rerun: not yet performed

## Review

- Evidence status: one reviewer; independent review pending
- Open question: compare the published selection procedure with validation-only epoch selection
