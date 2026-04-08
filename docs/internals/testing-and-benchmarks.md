# Testing and Benchmarks

## Test Strategy

The suite separates responsibilities:

- unit tests for pure rule/config/domain behavior
- integration tests for CLI and annotation snapshots
- resilience tests for failure boundaries and contract enforcement

Snapshot tests pin annotation behavior for selected fixtures and model version.

## Warm-Run Benchmark Record (Phase 3)

Benchmark harness:

- script: `tests/benchmarks/record_warm_run_benchmark.py`
- fixtures: `tests/fixtures/benchmarks/{small,medium,large}.md`
- record artifact: `tests/fixtures/benchmarks/warm_run_benchmark.json`

Run command:

```sh
conda run -n hermeneia python tests/benchmarks/record_warm_run_benchmark.py
```

The record stores:

- environment/model metadata
- fixture size metadata
- warm-run timing statistics (`runs_ms`, mean/median/min/max/p95)
- observed violation counts

Schema validation test:

- `tests/unit/test_benchmark_record.py`

The benchmark record keeps evidence versioned and CI-checkable without introducing
flaky runtime threshold assertions into normal test runs.
