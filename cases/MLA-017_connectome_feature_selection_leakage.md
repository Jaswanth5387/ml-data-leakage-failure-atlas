---
case_id: MLA-017
title: Connectome feature selection uses evaluation subjects before cross-validation
status: verified
confidence: confirmed
primary_mechanism: preprocessing
subtype: feature_selection_before_split
source_type: paper
source_url: https://doi.org/10.1038/s41467-024-46150-w
source_revision: doi:10.1038/s41467-024-46150-w
reproduction_status: static_verified
impact_basis: source_measured
---

# MLA-017 — Connectome feature selection uses evaluation subjects before cross-validation

## Source and task

- Study: *Data leakage inflates prediction performance in connectome-based machine learning models*
- Artifact: Nature Communications version of record, DOI 10.1038/s41467-024-46150-w
- Task: predict age, attention problems, and matrix reasoning from brain connectomes
- Intended boundary: outcome-informed feature selection must run independently inside every training fold
- Source license: CC BY 4.0

## Evidence

The [version-of-record study](https://doi.org/10.1038/s41467-024-46150-w) evaluates more than 400 pipelines across four datasets. Its feature-leakage condition selects features using combined training and test subjects; its gold-standard pipeline performs feature selection inside five-fold cross-validation.

## Information flow

Evaluation phenotypes influence which connectome edges are retained. The model is then tested on the same subjects whose outcomes helped define its input space.

## Why this is leakage

Supervised feature selection is part of model fitting. Running it before cross-validation lets test labels guide the model even when the final estimator never directly receives those labels.

## Impact

source_measured. For attention problems in HCPD, Pearson correlation rose from 0.01 to 0.48 and cross-validated R² rose from −0.13 to 0.22 under leaky feature selection. Across datasets and phenotypes, reported inflation reached Δr = 0.52 and ΔR² = 0.47. The atlas has not independently rerun the experiments.

## Correction

Place supervised selection inside the cross-validation pipeline. Fit the selector only on each training fold and apply the resulting mask unchanged to that fold's validation subjects.

## Reproduction

- Outcome: static verification of the paper's controlled pipelines and reported effects
- Date checked: 2026-08-21
- Independent atlas rerun: not yet performed

## Review

- Evidence status: one reviewer; independent review pending
- Open question: reproduce one public-dataset phenotype with the authors' linked code
