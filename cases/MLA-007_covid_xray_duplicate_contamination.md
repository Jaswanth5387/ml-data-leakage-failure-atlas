---
case_id: MLA-007
title: COVID chest X-ray corpus contains duplicate and near-duplicate images
status: verified
confidence: confirmed
primary_mechanism: contamination
subtype: near_duplicate
source_type: github
source_url: https://github.com/govindjeevan/COVID-Chest-X-Ray/blob/99d3f749e32b321c5bcfa319a21e546f7c6e3598/README.md
source_revision: 99d3f749e32b321c5bcfa319a21e546f7c6e3598
reproduction_status: static_verified
impact_basis: inferred
---

# MLA-007 — COVID chest X-ray corpus contains duplicate and near-duplicate images

## Source and task

- Project: `govindjeevan/COVID-Chest-X-Ray`
- Artifact: `README.md`, commit `99d3f74`, lines 121–134
- Task: classify chest X-rays as COVID-19, pneumonia, or normal
- Intended boundary: an image and its edited or augmented equivalents must stay in one partition
- Source license: not stated in the repository

## Evidence

The [pinned project report](https://github.com/govindjeevan/COVID-Chest-X-Ray/blob/99d3f749e32b321c5bcfa319a21e546f7c6e3598/README.md#L121-L134) reports 90 COVID-class images with exact or slightly edited duplicates. It explicitly identifies random cross-partition repetition as data leakage and groups related images to prevent it.

## Information flow

With a row- or file-level random split, an original image can enter training while an exact or edited copy enters validation or test. The model can then exploit image-specific content rather than generalize to a new patient image.

## Why this is leakage

Near-identical samples violate the independence of evaluation partitions. This is a real source-corpus contamination finding even though the reporting project detected and mitigated it before its final training procedure.

## Impact

`inferred`. The project describes overfitting risk but does not provide a controlled leaky-versus-deduplicated metric comparison in the cited report.

## Correction

Compute exact and perceptual hashes before splitting, confirm candidate groups, and assign each duplicate/augmentation group wholly to one partition. Prefer patient-level grouping when patient identifiers exist.

## Reproduction

- Outcome: static verification of the project's documented duplicate audit
- Date checked: 2026-08-21
- Independent rehash of the original image corpus: not yet performed

## Review

- Evidence status: one reviewer; independent review pending
- Open question: recover the exact source corpus and reproduce the 90-image duplicate count
