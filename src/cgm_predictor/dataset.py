"""Synthetic CGM cohort generation with contextual features."""

from __future__ import annotations

import math
import random


def generate_cohort(
    subjects: int = 24, readings: int = 140, seed: int = 31
) -> list[dict[str, float]]:
    rng = random.Random(seed)
    records: list[dict[str, float]] = []
    for subject in range(subjects):
        age = rng.uniform(19, 70)
        bmi = rng.uniform(19, 34)
        glucose = rng.uniform(88, 132) + max(bmi - 25, 0) * 1.4
        previous = glucose
        for step in range(readings):
            hour = (step * 5 / 60.0) % 24.0
            meal_window = min(abs(hour - center) for center in (8.0, 13.0, 20.0))
            carbs = rng.uniform(28, 68) if meal_window < 0.18 and rng.random() < 0.8 else 0.0
            activity = rng.uniform(0.5, 1.0) if 17.0 < hour < 19.5 and rng.random() < 0.35 else rng.uniform(0, 0.18)
            slope = glucose - previous
            circadian = math.sin((hour - 6.0) / 24.0 * 2.0 * math.pi)
            response = (
                0.56 * slope
                + carbs * 0.115
                - activity * 8.2
                + circadian * 0.70
                + (bmi - 25.0) * 0.025
                + rng.gauss(0, 1.65)
            )
            next_glucose = max(60.0, min(260.0, glucose + response))
            records.append(
                {
                    "subject": float(subject),
                    "glucose": glucose,
                    "previous": previous,
                    "slope": slope,
                    "carbs": carbs,
                    "activity": activity,
                    "sin_hour": math.sin(hour / 24.0 * 2.0 * math.pi),
                    "cos_hour": math.cos(hour / 24.0 * 2.0 * math.pi),
                    "age": age,
                    "bmi": bmi,
                    "target": next_glucose,
                }
            )
            previous, glucose = glucose, next_glucose
    return records


def split_by_subject(
    records: list[dict[str, float]], test_subject_fraction: float = 0.25
) -> tuple[list[dict[str, float]], list[dict[str, float]]]:
    subjects = sorted({int(row["subject"]) for row in records})
    boundary = max(1, int(len(subjects) * (1.0 - test_subject_fraction)))
    train_subjects = set(subjects[:boundary])
    return (
        [row for row in records if int(row["subject"]) in train_subjects],
        [row for row in records if int(row["subject"]) not in train_subjects],
    )


def matrix(
    records: list[dict[str, float]], featured: bool
) -> tuple[list[list[float]], list[float]]:
    if featured:
        names = (
            "glucose",
            "previous",
            "slope",
            "carbs",
            "activity",
            "sin_hour",
            "cos_hour",
            "age",
            "bmi",
        )
    else:
        names = ("glucose",)
    return [[row[name] for name in names] for row in records], [row["target"] for row in records]
