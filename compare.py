"""Compare two benchmark JSON files by median runtime."""
import argparse
import json
from pathlib import Path


def compare_results(baseline: dict, candidate: dict) -> float:
    if any(baseline[key] != candidate[key] for key in ("workload", "iterations")):
        raise ValueError("workload and iterations must match")
    if baseline["median_seconds"] <= 0 or candidate["median_seconds"] < 0:
        raise ValueError("median timings must be valid nonnegative numbers")
    return candidate["median_seconds"] / baseline["median_seconds"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("baseline", type=Path)
    parser.add_argument("candidate", type=Path)
    args = parser.parse_args()
    baseline = json.loads(args.baseline.read_text(encoding="utf-8"))
    candidate = json.loads(args.candidate.read_text(encoding="utf-8"))
    try:
        ratio = compare_results(baseline, candidate)
    except (KeyError, ValueError) as exc:
        parser.error(str(exc))
    print(f"Baseline median:  {baseline['median_seconds']:.6f} s")
    print(f"Candidate median: {candidate['median_seconds']:.6f} s")
    print(f"Candidate / baseline: {ratio:.3f}x")


if __name__ == "__main__":
    main()
