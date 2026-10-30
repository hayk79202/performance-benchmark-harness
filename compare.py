"""Compare two benchmark JSON files by median runtime."""
import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("baseline", type=Path)
    parser.add_argument("candidate", type=Path)
    args = parser.parse_args()
    baseline = json.loads(args.baseline.read_text(encoding="utf-8"))
    candidate = json.loads(args.candidate.read_text(encoding="utf-8"))
    keys = ("workload", "iterations")
    if any(baseline[key] != candidate[key] for key in keys):
        parser.error("workload and iterations must match")
    ratio = candidate["median_seconds"] / baseline["median_seconds"]
    print(f"Baseline median:  {baseline['median_seconds']:.6f} s")
    print(f"Candidate median: {candidate['median_seconds']:.6f} s")
    print(f"Candidate / baseline: {ratio:.3f}x")


if __name__ == "__main__":
    main()
