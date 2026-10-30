# Performance Benchmark Harness

![Python tests](https://github.com/hayk79202/performance-benchmark-harness/actions/workflows/ci.yml/badge.svg)

A repeatable Python benchmark runner for two small workloads: CPU arithmetic and memory allocation. It records raw timings and summary statistics as JSON so runs can be compared without inventing a performance claim.

## Run

```bash
python benchmark.py --workload cpu --iterations 100000 --samples 5 --output results/baseline.json
python benchmark.py --workload cpu --iterations 100000 --samples 5 --output results/candidate.json
python benchmark.py --workload memory --iterations 1000 --samples 5 --output results/memory.json
python compare.py results/baseline.json results/candidate.json
```

Python 3.10+ is enough; there are no third-party dependencies. A result includes the Python version, platform, workload, parameters, timestamp, per-sample seconds, median, and mean. `compare.py` prints a ratio of the two medians. Keep workload and iteration settings identical when comparing runs.

Add `--fail-above 1.10` to `compare.py` when you want an exit code of 1 for a candidate more than 10% slower. Small workloads can vary widely, so choose a threshold only after measuring on a controlled machine.

Run the behavior checks with `python -m unittest discover -s tests -v`. GitHub Actions runs these checks and a short sample benchmark on each push.

## Method

Each sample executes the same workload and is timed with `time.perf_counter()`. A warm-up run happens before recording. The CPU workload sums modular arithmetic; the memory workload allocates and reads a list. JSON files under `results/` are ignored because benchmark data is machine-specific.

## Scope and limits

This is a working command-line prototype, not a profiler or a statistically rigorous benchmark suite. It does not control CPU frequency, system load, affinity, or process isolation. There are no published benchmark numbers in this repository. Future work: process-level resource sampling, CI artifacts, and a reproducible Linux environment.

## License

MIT
