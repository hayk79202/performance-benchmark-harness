"""Small, dependency-free benchmark runner."""
import argparse
import json
import platform
import statistics
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


def run_workload(name: str, iterations: int) -> int:
    if name == "cpu":
        return sum((i * i) % 97 for i in range(iterations))
    if name == "memory":
        values = list(range(iterations))
        return sum(values)
    raise ValueError(f"unknown workload: {name}")


def benchmark(name: str, iterations: int, samples: int) -> dict:
    if iterations < 1 or samples < 1:
        raise ValueError("iterations and samples must be positive")
    run_workload(name, iterations)  # warm-up
    timings = []
    checksum = None
    for _ in range(samples):
        start = time.perf_counter()
        checksum = run_workload(name, iterations)
        timings.append(time.perf_counter() - start)
    return {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "platform": platform.platform(),
        "python": platform.python_version(),
        "workload": name,
        "iterations": iterations,
        "samples": samples,
        "seconds": timings,
        "median_seconds": statistics.median(timings),
        "mean_seconds": statistics.mean(timings),
        "checksum": checksum,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workload", choices=("cpu", "memory"), required=True)
    parser.add_argument("--iterations", type=int, default=100_000)
    parser.add_argument("--samples", type=int, default=5)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        result = benchmark(args.workload, args.iterations, args.samples)
    except ValueError as exc:
        parser.error(str(exc))
    payload = json.dumps(result, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload + "\n", encoding="utf-8")
    else:
        sys.stdout.write(payload + "\n")


if __name__ == "__main__":
    main()
