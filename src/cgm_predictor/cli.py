"""Evaluate a baseline and engineered CGM trend regression model."""

from __future__ import annotations

import argparse

from .dataset import generate_cohort, matrix, split_by_subject
from .regression import fit_ridge, predict, rmse


def evaluate(subjects: int, readings: int, seed: int) -> dict[str, float]:
    training, testing = split_by_subject(generate_cohort(subjects, readings, seed))
    base_train_x, train_y = matrix(training, featured=False)
    base_test_x, test_y = matrix(testing, featured=False)
    full_train_x, _ = matrix(training, featured=True)
    full_test_x, _ = matrix(testing, featured=True)
    baseline = rmse(test_y, predict(fit_ridge(base_train_x, train_y), base_test_x))
    featured = rmse(test_y, predict(fit_ridge(full_train_x, train_y), full_test_x))
    improvement = (baseline - featured) / baseline * 100.0
    results = {"baseline_rmse": baseline, "featured_rmse": featured, "improvement": improvement}
    print("CGM short-horizon trend prediction")
    print(f"Training rows: {len(training):,} | Test rows: {len(testing):,}")
    print(f"Current-reading baseline RMSE: {baseline:.3f} mg/dL")
    print(f"Engineered-feature RMSE:      {featured:.3f} mg/dL")
    print(f"RMSE improvement:              {improvement:.1f}%")
    print("\nResearch demonstration only; not for clinical decision-making.")
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--subjects", type=int, default=24)
    parser.add_argument("--readings", type=int, default=140)
    parser.add_argument("--seed", type=int, default=31)
    args = parser.parse_args()
    evaluate(args.subjects, args.readings, args.seed)


if __name__ == "__main__":
    main()
