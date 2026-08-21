---
case_id: MLA-015
title: Panel-data forecasting uses future periods and contemporaneous predictors
status: verified
confidence: confirmed
primary_mechanism: temporal
subtype: random_time_split
source_type: paper
source_url: https://arxiv.org/abs/2411.09218v2
source_revision: arXiv:2411.09218v2
reproduction_status: static_verified
impact_basis: source_measured
---

# MLA-015 — Panel-data forecasting uses future periods and contemporaneous predictors

## Source and task

- Study: *On the (Mis)Use of Machine Learning with Panel Data*
- Artifact: arXiv version 2, arXiv:2411.09218v2
- Task: forecast county-level recessions and income using more than 3,000 US counties from 2000–2019
- Intended boundary: training observations and predictors must be available before the forecast year
- Source license: article license linked from the arXiv record

## Evidence

The [frozen paper version](https://arxiv.org/abs/2411.09218v2) compares 480 models. Its leaky configurations use observation-level random splits, which place later years in training than some test observations, and/or contemporaneous predictors such as unemployment from the same year as the income target. The corrected configurations split on time and exclude contemporaneous predictors.

## Information flow

Future observations reveal trends and structural changes to models evaluated on earlier years. Same-year predictors can also reflect the event the model is supposed to forecast.

## Why this is leakage

A genuine forecast can use only information available before the prediction date. Random panel splitting and contemporaneous predictors turn a forecasting task partly into retrospective estimation.

## Impact

source_measured. Average Random Forest AUC was 0.759 for temporally leaked configurations versus 0.708 without leakage. For the 2009 recession, AUC fell from 0.692 to 0.442. The source also reports an XGBoost regression leakage ratio greater than 17%. The atlas has not independently rerun the experiments.

## Correction

Use an expanding or fixed chronological split, fit all transformations inside the training period, and lag predictors so their publication time precedes the forecast origin.

## Reproduction

- Outcome: static verification of the frozen paper's design and reported comparisons
- Date checked: 2026-08-21
- Independent atlas rerun: not yet performed

## Review

- Evidence status: one reviewer; independent review pending
- Open question: obtain the authors' analysis code and reproduce the 480-model grid
