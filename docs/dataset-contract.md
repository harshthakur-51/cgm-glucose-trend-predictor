# CGM Dataset Contract

This contract defines the preferred CSV format for the next version of the CGM glucose trend predictor. The model can adapt to a different file, but every column must have clear units and timing semantics before training.

## Required Columns

| Column | Type | Notes |
| --- | --- | --- |
| `subject_id` | string | Stable de-identified patient/participant ID. Required for leakage-safe splitting. |
| `timestamp` | datetime | Local or UTC timestamp; timezone should be documented. |
| `glucose_mg_dl` | float | Current CGM glucose value in mg/dL. |

If `subject_id` is unavailable, use a de-identified `session_id` and a time-forward split. Do not mix rows from the same continuous session across train and test sets.

## Strongly Recommended Columns

| Column | Type | Notes |
| --- | --- | --- |
| `session_id` | string | Sensor wear/session identifier if available. |
| `age` | float | Optional demographic context. |
| `sex` | category | Optional; useful for subgroup error checks. |
| `bmi` | float | Optional metabolic context. |
| `insulin_units` | float | Dose amount aligned to timestamp/event. |
| `carbs_g` | float | Meal carbohydrate amount. |
| `activity_level` | float/category | Activity intensity, steps, MET estimate, or encoded activity class. |
| `event_type` | category | Example: reading, meal, insulin, exercise. |

## Generated Columns

The training pipeline can create these automatically:

| Column | Meaning |
| --- | --- |
| `target_glucose_15m` | Glucose shifted 15 minutes into the future. |
| `target_glucose_30m` | Glucose shifted 30 minutes into the future. |
| `target_glucose_60m` | Glucose shifted 60 minutes into the future. |
| `trend_class` | Falling, stable, rising, or risk class generated from future delta. |
| `glucose_slope` | Recent rate of change. |
| `rolling_mean_*` | Rolling mean windows. |
| `rolling_std_*` | Recent volatility. |

## Validation Rules

- Timestamps must be parseable and sorted within each subject/session.
- Glucose values must have documented units.
- Duplicate `(subject_id, timestamp)` rows should be reported.
- Missing glucose values should be flagged before imputation.
- Future target rows at the end of each subject/session should be excluded from supervised training.
- Train/test splits must be subject-level when `subject_id` exists.

## Data Safety Notes

- Use only de-identified data.
- Do not commit private health information.
- Do not commit raw clinical datasets unless the license and consent allow public release.
- Public examples should use synthetic or approved open data.
