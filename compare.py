"""Compare two benchmark JSON files by median runtime."""
import argparse
import json
import math
import sys
from pathlib import Path


def compare_results(baseline: dict, candidate: dict) -> float:
    if any(baseline[key] != candidate[key] for key in ("workload", "iterations")):
        raise ValueError("workload and iterations must match")
    base_time = baseline["median_seconds"]
    candidate_time = candidate["median_seconds"]
    if not math.isfinite(base_time) or not math.isfinite(candidate_time) or base_time <= 0 or candidate_time < 0:
        raise ValueError("median timings must be finite and nonnegative; baseline must be positive")
    return candidate_time / base_time


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("baseline", type=Path)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--fail-above", type=float, help="Exit 1 if candidate/baseline exceeds this ratio")
    args = parser.parse_args()
    if args.fail_above is not None and (not math.isfinite(args.fail_above) or args.fail_above <= 0):
        parser.error("--fail-above must be finite and positive")
    baseline = json.loads(args.baseline.read_text(encoding="utf-8"))
    candidate = json.loads(args.candidate.read_text(encoding="utf-8"))
    try:
        ratio = compare_results(baseline, candidate)
    except (KeyError, TypeError, ValueError) as exc:
        parser.error(str(exc))
    print(f"Baseline median:  {baseline['median_seconds']:.6f} s")
    print(f"Candidate median: {candidate['median_seconds']:.6f} s")
    print(f"Candidate / baseline: {ratio:.3f}x")
    if args.fail_above is not None and ratio > args.fail_above:
        print(f"Regression threshold exceeded: {args.fail_above:.3f}x", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
