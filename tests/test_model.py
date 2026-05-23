import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from cgm_predictor.cli import evaluate
from cgm_predictor.dataset import generate_cohort, split_by_subject


class ModelTests(unittest.TestCase):
    def test_subject_split_has_no_leakage(self):
        training, testing = split_by_subject(generate_cohort(subjects=8, readings=10))
        train_ids = {row["subject"] for row in training}
        test_ids = {row["subject"] for row in testing}
        self.assertFalse(train_ids & test_ids)

    def test_featured_model_beats_baseline(self):
        results = evaluate(subjects=18, readings=100, seed=31)
        self.assertGreater(results["improvement"], 20.0)


if __name__ == "__main__":
    unittest.main()
