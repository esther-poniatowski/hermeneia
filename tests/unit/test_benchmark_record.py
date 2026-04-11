from __future__ import annotations

import json
from pathlib import Path

BENCHMARK_RECORD = (
    Path(__file__).resolve().parents[1] / "fixtures" / "benchmarks" / "warm_run_benchmark.json"
)
EXPECTED_FIXTURES = {"small.md", "medium.md", "large.md"}


def test_warm_run_benchmark_record_exists_and_matches_schema() -> None:
    assert BENCHMARK_RECORD.exists()
    payload = json.loads(BENCHMARK_RECORD.read_text(encoding="utf-8"))

    assert payload["benchmark_name"] == "phase3_warm_run_latency"
    assert isinstance(payload["recorded_at_utc"], str)

    harness = payload["harness"]
    assert harness["script"] == "tests/benchmarks/record_warm_run_benchmark.py"
    assert isinstance(harness["iterations"], int)
    assert harness["iterations"] >= 1

    environment = payload["environment"]
    assert environment["language_pack"] == "en"
    assert environment["spacy_model"] == "en_core_web_sm"
    assert environment["spacy_model_package"] == "en-core-web-sm"

    fixtures = payload["fixtures"]
    assert isinstance(fixtures, list)
    assert {entry["fixture"] for entry in fixtures} == EXPECTED_FIXTURES

    for entry in fixtures:
        size = entry["size"]
        assert size["chars"] > 0
        assert size["lines"] > 0
        assert size["paragraphs"] > 0
        assert size["words"] > 0

        timing = entry["warm_run_ms"]
        runs = timing["runs_ms"]
        assert isinstance(runs, list)
        assert len(runs) == harness["iterations"]
        assert all(value > 0 for value in runs)
        assert timing["min"] <= timing["median"] <= timing["max"]
        assert timing["min"] <= timing["mean"] <= timing["max"]
        assert timing["min"] <= timing["p95"] <= timing["max"]

        assert isinstance(entry["violation_count"], int)
        assert entry["violation_count"] >= 0
