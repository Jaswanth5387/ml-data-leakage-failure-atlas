---
case_id: MLA-018
title: EEG augmentation sends segments from the same patient across folds
status: verified
confidence: confirmed
primary_mechanism: contamination
subtype: augmentation_overlap
source_type: paper
source_url: https://doi.org/10.1038/s41598-023-43542-8
source_revision: doi:10.1038/s41598-023-43542-8
reproduction_status: static_verified
impact_basis: source_measured
---

# MLA-018 — EEG augmentation sends segments from the same patient across folds

## Source and task

- Study: *Risk of data leakage in estimating the diagnostic performance of a deep-learning-based computer-aided system for psychiatric disorders*
- Artifact: Scientific Reports version of record, DOI 10.1038/s41598-023-43542-8
- Task: distinguish 77 PTSD patients from 58 healthy controls using cropped resting-state EEG
- Intended boundary: every segment derived from one participant must remain in one fold
- Source license: CC BY 4.0

## Evidence

The [version-of-record study](https://doi.org/10.1038/s41598-023-43542-8) compares subject-wise CV with trial-wise CV after cropping each participant's 60-second EEG into shorter segments. Trial-wise CV randomly distributes segments from the same participant across training and test; the overlapped version uses windows with 75% overlap.

## Information flow

Training contains segments with the same participant-specific signal—and sometimes overlapping time samples—as test segments. The network can recognize the participant rather than learn a general PTSD marker.

## Why this is leakage

The deployment unit is a new patient, not a new crop from a known recording. Segment-level randomization violates that patient-level boundary.

## Impact

source_measured. Trial-wise and overlapped trial-wise CV inflated CNN-13 accuracy by roughly 5–15 percentage points and EEGNet accuracy by roughly 15–20 points relative to subject-wise CV. Differences were statistically significant for augmented window lengths. The atlas has not independently rerun the experiments.

## Correction

Assign participants to folds before cropping. Generate all augmented windows inside their participant's assigned partition and never move derived segments across folds.

## Reproduction

- Outcome: static verification of the paper's controlled CV comparison
- Date checked: 2026-08-21
- Independent atlas rerun: not yet performed; data are available from the authors on request

## Review

- Evidence status: one reviewer; independent review pending
- Open question: reproduce the subject-wise and trial-wise comparison after obtaining the EEG data
