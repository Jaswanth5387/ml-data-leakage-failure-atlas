---
case_id: MLA-014
title: Stroke classifier learns the target from systematic missingness
status: verified
confidence: confirmed
primary_mechanism: target
subtype: missingness_proxy
source_type: paper
source_url: https://doi.org/10.1038/s41598-025-16660-8
source_revision: doi:10.1038/s41598-025-16660-8
reproduction_status: static_verified
impact_basis: source_measured
---

# MLA-014 — Stroke classifier learns the target from systematic missingness

## Source and task

- Study: *A novel machine learning framework for stroke type identification in resource constrained settings with robustness to missing data*
- Artifact: Scientific Reports version of record, DOI 10.1038/s41598-025-16660-8
- Task: distinguish ischemic from hemorrhagic stroke using clinical attributes
- Intended boundary: predictors must not encode how clinicians recorded the confirmed stroke type
- Source license: CC BY-NC-ND 4.0

## Evidence

The [version-of-record article](https://doi.org/10.1038/s41598-025-16660-8) reports that NIHSS was collected for ischemic cases but not hemorrhagic cases. A model could therefore infer the target from whether NIHSS was missing. The study obtained essentially the same high performance with that single attribute and identified serum homocysteine as a second leakage-prone field.

## Information flow

The confirmed stroke type affected which measurements were recorded. Missingness was then exposed to the model, creating a near-direct proxy for the outcome.

## Why this is leakage

The model learned the data-collection process after diagnosis rather than a deployable clinical relationship available before the target was known.

## Impact

source_measured. Weighted accuracy was 97.3% before the leakage audit. After removing the two principal leakage attributes, the best full-feature experiments reached 80.84%; the controlled source comparison therefore shows a 16.46 percentage-point reduction. The atlas has not independently rerun the experiment.

## Correction

Audit missingness by class and by collection time. Remove fields whose availability depends on the confirmed outcome, then validate on prospectively collected patients.

## Reproduction

- Outcome: static verification of the paper's methods and controlled results
- Date checked: 2026-08-21
- Independent atlas rerun: not yet performed; the underlying clinical data require author access

## Review

- Evidence status: one reviewer; independent review pending
- Open question: reproduce the ablation if the retrospective dataset becomes available
