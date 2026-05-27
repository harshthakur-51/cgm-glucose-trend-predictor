# CGM Model Improvement Roadmap

This document converts the assignment prototype into a stronger engineering plan for a reproducible glucose trend prediction system. The current repository is a synthetic demonstration; the next iteration should be driven by a de-identified CSV dataset with a documented schema and leakage-safe evaluation.

This work is for research and engineering demonstration only. It is not a medical device, diagnostic tool, or insulin dosing system.

## Starting Point From The Submission

The reference submission describes a backend/API proof of concept for continuous glucose monitoring prediction. It compares Random Forest, Support Vector Regression, and LSTM-style sequence modeling, with reported evaluation using MAE, RMSE, and R2.

Core idea to preserve:

- Predict glucose or near-future glucose trend from CGM history and patient/context features.
- Keep a backend-ready model artifact for app integration.
- Compare classical ML models against time-series models.

Main gaps to improve:

- Replace broad claims with reproducible experiments.
- Use patient-aware train/test splits to prevent leakage.
- Add time-series windows, horizon definitions, and calibration checks.
- Report uncertainty and subgroup performance, not only one aggregate score.
- Keep API deployment reproducible instead of relying on temporary tunnel links.

## Target Prediction Tasks

Recommended first version:

- Regression: predict glucose value at a fixed horizon, such as 15, 30, or 60 minutes ahead.
- Classification: predict trend class, such as falling, stable, rising, or urgent-risk band.
- Risk flag: detect possible hypo/hyperglycemic risk in the next horizon.

The CSV should make the prediction horizon explicit. If the raw file only has timestamps and glucose readings, the pipeline can generate future labels by shifting each subject time series.

## Data Pipeline

The production-quality pipeline should include:

- CSV schema validation before training.
- Timestamp parsing and sorting per subject/session.
- Unit checks for glucose, insulin, carbohydrate, activity, and time intervals.
- Missing-value report with explicit imputation strategy.
- Outlier flags rather than silent deletion.
- Subject-level or session-level train/validation/test split.
- Optional rolling-window feature generation.

Leakage rule: never let future glucose values, future meal records, or the same subject-session leak into training features for a prediction target.

## Feature Engineering

Baseline features:

- Current glucose.
- Lagged glucose values.
- Short and medium rolling means.
- Glucose slope and acceleration.
- Time since previous reading.
- Circadian features from timestamp.

Contextual features, if available:

- Age, sex, BMI, diabetes type.
- Insulin dose and time since dose.
- Meal/carbohydrate amount and time since meal.
- Activity intensity and duration.
- Sleep/rest indicator.
- Sensor/session identifier for quality analysis.

Derived safety features:

- Rate of change in mg/dL per minute.
- Recent volatility.
- Time spent below/above threshold.
- Data quality flags for missing windows or irregular sampling.

## Model Ladder

Build from simple to advanced so each improvement earns its place.

1. Naive persistence baseline
   - Predict that future glucose equals current glucose.
   - This is mandatory for judging whether ML actually helps.

2. Linear and regularized models
   - Ridge, Lasso, Elastic Net.
   - Useful for interpretability and fast debugging.

3. Tree-based models
   - Random Forest.
   - Gradient boosting if dependencies are allowed later.
   - Strong tabular baseline for engineered features.

4. Support Vector Regression
   - Useful comparison model, but can be slow on large datasets.

5. Sequence models
   - LSTM/GRU/TCN for fixed windows of CGM history.
   - Only add after the classical pipeline is reproducible.

6. Hybrid ensemble
   - Combine engineered-feature model with sequence model outputs.
   - Use a validation set for blending, not the test set.

## Evaluation

Primary regression metrics:

- MAE in mg/dL.
- RMSE in mg/dL.
- R2 for broad comparison.
- Median absolute error for robustness.

Biomedical measurement checks:

- Bland-Altman plot or summary statistics.
- Clarke/Parkes-style risk zones if clinically appropriate and sourced later.
- Error by glucose range: low, normal, high.
- Error by horizon: 15, 30, 60 minutes.

Operational checks:

- Inference latency.
- Model artifact size.
- Missing-input behavior.
- API response schema stability.

Validation strategy:

- Subject-level split when subject IDs exist.
- Time-forward split when subject IDs are unavailable.
- Cross-validation only inside the training set.
- Final test set touched once for reporting.

## Backend/API Direction

Recommended API endpoints:

- `GET /health`: service status and model version.
- `POST /predict`: returns predicted glucose, trend, risk flag, and confidence band.
- `POST /batch-predict`: optional endpoint for offline evaluation.

Recommended response fields:

- `prediction_mg_dl`
- `horizon_minutes`
- `trend_class`
- `risk_level`
- `confidence_low_mg_dl`
- `confidence_high_mg_dl`
- `model_version`
- `warnings`

For public demo deployment, prefer a reproducible local/API runner. Temporary tunneling can be documented as a demo option, but it should not be the core deployment story.

## Repository Upgrade Plan

Suggested structure for the next commit series:

```text
src/cgm_predictor/
  data_contract.py
  preprocessing.py
  features.py
  splits.py
  models/
    baselines.py
    sklearn_models.py
    sequence_models.py
  evaluation.py
  api.py
notebooks/
  01_data_audit.ipynb
  02_model_comparison.ipynb
reports/
  figures/
tests/
  test_data_contract.py
  test_splits.py
  test_features.py
```

Minimum tests before calling the project serious:

- Schema validation rejects missing critical columns.
- Feature generation does not use future readings.
- Subject-level split keeps subjects separated.
- Baseline metrics are reproducible on a fixture dataset.
- API returns stable JSON for valid and invalid payloads.

## Once The CSV Arrives

First actions:

1. Identify columns, units, sampling interval, subject/session IDs, and target availability.
2. Create a data dictionary and schema validator.
3. Run a data audit: missingness, duplicates, timestamp gaps, outliers, subject counts.
4. Define prediction horizons and generate labels.
5. Establish persistence baseline before training heavier models.
6. Compare models with leakage-safe splits.
7. Publish a concise model card with honest limitations.
