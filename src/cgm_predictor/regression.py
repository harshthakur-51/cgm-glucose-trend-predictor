"""Minimal ridge regression utilities for a transparent portfolio model."""

from __future__ import annotations

import math


def _solve(system: list[list[float]], values: list[float]) -> list[float]:
    size = len(values)
    augmented = [row[:] + [value] for row, value in zip(system, values)]
    for pivot in range(size):
        best = max(range(pivot, size), key=lambda index: abs(augmented[index][pivot]))
        augmented[pivot], augmented[best] = augmented[best], augmented[pivot]
        divisor = augmented[pivot][pivot]
        if abs(divisor) < 1e-12:
            raise ValueError("Singular regression system")
        augmented[pivot] = [value / divisor for value in augmented[pivot]]
        for row in range(size):
            if row == pivot:
                continue
            factor = augmented[row][pivot]
            augmented[row] = [
                value - factor * pivot_value
                for value, pivot_value in zip(augmented[row], augmented[pivot])
            ]
    return [row[-1] for row in augmented]


def fit_ridge(rows: list[list[float]], targets: list[float], penalty: float = 0.01) -> list[float]:
    augmented = [[1.0] + row for row in rows]
    columns = len(augmented[0])
    gram = [[0.0 for _ in range(columns)] for _ in range(columns)]
    projected = [0.0 for _ in range(columns)]
    for row, target in zip(augmented, targets):
        for i in range(columns):
            projected[i] += row[i] * target
            for j in range(columns):
                gram[i][j] += row[i] * row[j]
    for index in range(1, columns):
        gram[index][index] += penalty
    return _solve(gram, projected)


def predict(weights: list[float], rows: list[list[float]]) -> list[float]:
    return [weights[0] + sum(value * weight for value, weight in zip(row, weights[1:])) for row in rows]


def rmse(actual: list[float], predicted: list[float]) -> float:
    return math.sqrt(sum((a - p) ** 2 for a, p in zip(actual, predicted)) / len(actual))
