# Leakage taxonomy

The primary label describes how information crosses the evaluation boundary. A case may have secondary labels, but one primary mechanism is required.

## Target leakage (`target`)

Features contain the label, a transformation of it, or information only created after the outcome.

- `direct_target`: the label or an equivalent field appears in the features.
- `target_aggregate`: target statistics use evaluation rows or labels.
- `post_outcome_feature`: a feature is unavailable until after the predicted event.
- `label_in_pretraining`: evaluation labels enter a learned representation or prompt corpus.

## Temporal leakage (`temporal`)

Training or feature generation uses information unavailable at the prediction timestamp.

- `future_observation`: a future value is used directly.
- `future_aggregate`: a rolling, grouped, or cumulative statistic includes future records.
- `random_time_split`: a random split breaks a chronological deployment boundary.
- `revision_leakage`: revised data unavailable at the historical decision time is used.

## Preprocessing leakage (`preprocessing`)

A data-dependent transformation is fitted outside the training partition.

- `scaling_before_split`
- `imputation_before_split`
- `feature_selection_before_split`
- `dimensionality_reduction_before_split`
- `encoding_before_split`
- `resampling_before_split`

## Dataset contamination (`contamination`)

Evaluation samples, entities, or near-equivalents also appear in training.

- `exact_duplicate`
- `near_duplicate`
- `entity_overlap`
- `group_overlap`
- `augmentation_overlap`
- `external_data_overlap`

## Evaluation leakage (`evaluation`)

Evaluation labels or metrics influence model, checkpoint, threshold, or hyperparameter selection.

- `test_set_model_selection`: test performance chooses among models, epochs, or configurations.
- `test_set_early_stopping`: the test set is supplied to a training-time callback or stopping rule.
- `test_set_hyperparameter_tuning`: test performance directly tunes hyperparameters or thresholds.

## Confidence labels

| Label | Meaning |
|---|---|
| `confirmed` | The information path is demonstrated and the intended boundary is established. |
| `probable` | Evidence strongly supports leakage, but one material fact cannot be independently checked. |
| `ambiguous` | The pattern is concerning, but task semantics or data provenance do not establish leakage. |

Ambiguous records may remain in the research log, but they are excluded from the headline verified-case count.

## Impact labels

- `measured`: leaky and corrected pipelines were compared under a controlled rerun.
- `inferred`: the direction of bias follows from the information path, but magnitude was not measured.
- `unknown`: available artifacts do not support an impact claim.
