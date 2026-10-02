from __future__ import annotations

import unittest

from emb.core import load_cases, reference_predictions, score


class BenchmarkTests(unittest.TestCase):
    def setUp(self) -> None:
        self.cases = load_cases()

    def test_public_corpus_has_domain_breadth(self) -> None:
        self.assertGreaterEqual(len(self.cases), 10)
        self.assertGreaterEqual(len({case["domain"] for case in self.cases}), 7)

    def test_reference_predictions_pass_every_floor(self) -> None:
        report = score(self.cases, reference_predictions(self.cases))
        self.assertTrue(report["passed"])
        self.assertEqual(report["overall"], 1.0)
        self.assertEqual(report["critical_failures"], [])

    def test_unknown_claim_is_a_critical_failure(self) -> None:
        predictions = reference_predictions(self.cases)
        predictions[0]["claims"].append({"id": "invented_claim", "cited_record_ids": []})
        report = score(self.cases, predictions)
        self.assertFalse(report["passed"])
        self.assertTrue(any("unknown claim" in item for item in report["critical_failures"]))

    def test_forbidden_record_exposure_is_a_critical_failure(self) -> None:
        predictions = reference_predictions(self.cases)
        target_index = next(
            index for index, case in enumerate(self.cases)
            if case["expected"]["forbidden_output_record_ids"]
        )
        forbidden = self.cases[target_index]["expected"]["forbidden_output_record_ids"][0]
        predictions[target_index]["retrieved_record_ids"].append(forbidden)
        report = score(self.cases, predictions)
        self.assertFalse(report["passed"])
        self.assertTrue(any("forbidden" in item for item in report["critical_failures"]))


if __name__ == "__main__":
    unittest.main()
