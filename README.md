# CGM Glucose Trend Predictor

A reproducible machine-learning demonstration for forecasting short-horizon glucose
trends from continuous glucose monitoring (CGM) observations and contextual inputs.
It compares a current-reading-only baseline against an engineered-feature ridge
regression model.

This repository uses a synthetic cohort and is intended for engineering and
research demonstration only. It is not a medical device and must not be used for
treatment or dosing decisions.

## Model inputs

- Current and preceding CGM readings
- Recent glucose slope
- Carbohydrate event estimate
- Activity intensity estimate
- Circadian time features
- Demographic context (`age` and `bmi`)

## Run the experiment

```bash
python -m cgm_predictor.cli --subjects 24 --readings 140
```

Install with `python -m pip install -e .`, or expose `src` on `PYTHONPATH`.
The implementation is dependency-free Python so it can run in minimal
environments.

## Test

```bash
python -m unittest discover -s tests -v
```

## Repository structure

- `dataset.py`: controlled synthetic cohort generation and feature matrices.
- `regression.py`: ridge-regression fitting, prediction, and RMSE calculation.
- `cli.py`: baseline-versus-featured evaluation report.

For a clinical or academic extension, replace `generate_cohort` with an approved,
de-identified dataset adapter while retaining the evaluation boundary.
