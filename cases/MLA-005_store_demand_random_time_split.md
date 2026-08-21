---
case_id: MLA-005
title: Store-demand forecast uses a shuffled random holdout
status: verified
confidence: confirmed
primary_mechanism: temporal
subtype: random_time_split
source_type: github
source_url: https://github.com/jhihan/Store-Item-Demand-Forecasting-Challenge/blob/7b43f6e49f99443290cca4a53b97f01e280d0bd2/Store_Item_Demand_Forecasting.ipynb
source_revision: 7b43f6e49f99443290cca4a53b97f01e280d0bd2
reproduction_status: static_verified
impact_basis: inferred
---

# MLA-005 — Store-demand forecast uses a shuffled random holdout

## Source and task

- Project: `jhihan/Store-Item-Demand-Forecasting-Challenge`
- Artifact: `Store_Item_Demand_Forecasting.ipynb`, commit `7b43f6e`, cells 12 and 35
- Task: forecast 2018 daily item sales from 2013–2017 history
- Intended boundary: training dates must precede validation dates
- Source license: not stated in the repository

## Evidence

Cell 12 of the [pinned notebook](https://github.com/jhihan/Store-Item-Demand-Forecasting-Challenge/blob/7b43f6e49f99443290cca4a53b97f01e280d0bd2/Store_Item_Demand_Forecasting.ipynb) states that training covers 2013–2017 and test covers the first quarter of 2018. Cell 35 uses `train_test_split(..., random_state=42)` without `shuffle=False`; scikit-learn's default is `shuffle=True`.

## Information flow

The random holdout mixes dates. Some later observations become training rows while earlier observations become validation rows, so the offline evaluation does not simulate forecasting the future from the past.

## Why this is leakage

Scikit-learn's [time-series example](https://scikit-learn.org/stable/auto_examples/applications/plot_time_series_lagged_features.html) shows that default shuffled splitting can produce overly optimistic errors for forecasting. `TimeSeriesSplit` exists because ordinary cross-validation can train on future data and evaluate on the past.

## Impact

`inferred`. The validation error may be optimistic. The magnitude is not measured here.

## Correction

Sort by date and reserve the latest contiguous window as validation, or use expanding-window `TimeSeriesSplit`. Keep every store-item series aligned to the same cutoff and recompute lag features within each training window.

## Reproduction

- Outcome: static task-boundary and split-default verification
- Date checked: 2026-08-21
- Controlled rerun: not yet performed

## Review

- Evidence status: one reviewer; independent review pending
- Open question: compare random-holdout SMAPE against the final contiguous validation period
