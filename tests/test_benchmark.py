import unittest

from benchmark import benchmark, run_workload
from compare import compare_results


class BenchmarkTests(unittest.TestCase):
    def test_workloads_are_deterministic(self):
        self.assertEqual(run_workload("memory", 4), 6)
        self.assertEqual(run_workload("cpu", 4), 14)
        with self.assertRaises(ValueError):
            run_workload("unknown", 4)

    def test_benchmark_records_every_sample(self):
        result = benchmark("cpu", 100, 3)
        self.assertEqual(result["samples"], 3)
        self.assertEqual(len(result["seconds"]), 3)
        self.assertGreater(result["median_seconds"], 0)
        self.assertEqual(result["checksum"], run_workload("cpu", 100))
        with self.assertRaises(ValueError):
            benchmark("cpu", 0, 3)

    def test_compare_requires_matching_settings(self):
        baseline = {"workload": "cpu", "iterations": 100, "median_seconds": 2.0}
        candidate = {"workload": "cpu", "iterations": 100, "median_seconds": 1.0}
        self.assertEqual(compare_results(baseline, candidate), 0.5)
        with self.assertRaises(ValueError):
            compare_results(baseline, {**candidate, "iterations": 200})
        with self.assertRaises(ValueError):
            compare_results({**baseline, "median_seconds": 0}, candidate)


if __name__ == "__main__":
    unittest.main()
