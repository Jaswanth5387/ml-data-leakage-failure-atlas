---
case_id: MLA-016
title: OCT image splits place slices from the same subject in training and test
status: verified
confidence: confirmed
primary_mechanism: contamination
subtype: group_overlap
source_type: paper
source_url: https://doi.org/10.1038/s41597-022-01618-6
source_revision: doi:10.1038/s41597-022-01618-6
reproduction_status: static_verified
impact_basis: source_measured
---

# MLA-016 — OCT image splits place slices from the same subject in training and test

## Source and task

- Study: *Inflation of test accuracy due to data leakage in deep learning-based classification of OCT images*
- Artifact: Scientific Data version of record, DOI 10.1038/s41597-022-01618-6
- Task: classify retinal and breast-tissue OCT images across three public datasets
- Intended boundary: all slices from one volume or subject must remain in one partition
- Source license: CC BY 4.0

## Evidence

The [version-of-record study](https://doi.org/10.1038/s41597-022-01618-6) compares per-image splitting with volume/subject-level splitting. Consecutive OCT slices share anatomy and acquisition noise. The authors also found that 92% of test images in Kermany OCT2017 version 2 had subject IDs present in training.

## Information flow

Random image-level splitting lets a model train on neighboring slices or related images from the same acquisition that produced its test samples.

## Why this is leakage

The intended claim is generalization to a new subject or scan. Test slices are not independent when the model has already seen highly related slices from that subject or volume.

## Impact

source_measured. Improper splits inflated accuracy by 5–30 percentage points and MCC by 0.07–0.43 across the tested datasets. The atlas has not independently rerun the experiments.

## Correction

Create groups from subject and acquisition identifiers before any image sampling or augmentation. Assign complete groups to folds and verify that no identifier or perceptual-neighbor group crosses a boundary.

## Reproduction

- Outcome: static verification of the paper's controlled split comparison
- Date checked: 2026-08-21
- Independent atlas rerun: not yet performed

## Review

- Evidence status: one reviewer; independent review pending
- Open question: reproduce the published LightOCT experiments from the linked public code
