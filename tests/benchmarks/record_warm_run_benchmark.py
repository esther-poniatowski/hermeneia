"""Record warm-run analysis latency on representative benchmark fixtures.

Usage:
    conda run -n hermeneia python tests/benchmarks/record_warm_run_benchmark.py
"""

from __future__ import annotations

from argparse import ArgumentParser
from datetime import datetime, timezone
from importlib import metadata
import json
from pathlib import Path
from statistics import mean, median
import sys
from time import perf_counter

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from hermeneia.config.profile import ProfileResolver
from hermeneia.config.schema import ProjectConfig
from hermeneia.document.annotator import SpaCyDocumentAnnotator
from hermeneia.document.markdown import MarkdownDocumentParser
from hermeneia.engine.registry import RuleRegistry
from hermeneia.engine.runner import AnalysisInput, AnalysisRunner
from hermeneia.language.en import ENGLISH_SPACY_MODEL_VERSION
from hermeneia.language.registry import LanguageRegistry
from hermeneia.rules.loader import load_builtin_rules


def main() -> None:
    args = _parse_args()
    fixtures_dir = args.fixtures_dir.resolve()
    output_path = args.output.resolve()
    fixture_paths = tuple(
        sorted(path for path in fixtures_dir.glob("*.md") if path.is_file())
    )
    if not fixture_paths:
        raise RuntimeError(f"No benchmark fixtures found in {fixtures_dir}")

    language_pack = LanguageRegistry().get("en")
    registry = RuleRegistry()
    load_builtin_rules(registry)
    profile = ProfileResolver(registry).resolve(ProjectConfig(), language_pack)

    runner = AnalysisRunner(
        parser=MarkdownDocumentParser(language_pack),
        annotator=SpaCyDocumentAnnotator(language_pack.parser_model),
        registry=registry,
        language_pack=language_pack,
        embedding_backend=None,
    )

    fixtures_payload: list[dict[str, object]] = []
    for fixture in fixture_paths:
        source = fixture.read_text(encoding="utf-8")
        input_item = AnalysisInput(path=fixture, source=source)

        # Warm once to exclude first-load effects from warm-run measurement.
        runner.analyze((input_item,), profile)

        durations_ms: list[float] = []
        last_violation_count = 0
        for _ in range(args.iterations):
            start = perf_counter()
            batch = runner.analyze((input_item,), profile)
            durations_ms.append((perf_counter() - start) * 1000.0)
            if batch.results:
                last_violation_count = len(batch.results[0].violations)

        fixtures_payload.append(
            {
                "fixture": fixture.name,
                "size": _size_payload(source),
                "warm_run_ms": _duration_payload(durations_ms),
                "violation_count": last_violation_count,
            }
        )

    payload = {
        "benchmark_name": "phase3_warm_run_latency",
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "harness": {
            "script": str(Path(__file__).relative_to(ROOT)),
            "iterations": args.iterations,
            "notes": "Warm-run latency per document after a single warmup run.",
        },
        "environment": {
            "python_version": sys.version.split()[0],
            "platform": sys.platform,
            "language_pack": language_pack.code,
            "spacy_model": language_pack.parser_model,
            "spacy_model_package": "en-core-web-sm",
            "spacy_model_version": ENGLISH_SPACY_MODEL_VERSION,
            "spacy_model_installed_version": _safe_package_version("en-core-web-sm"),
        },
        "fixtures": fixtures_payload,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote warm-run benchmark record: {output_path}")


def _parse_args():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument(
        "--iterations",
        type=int,
        default=5,
        help="Number of timed warm runs per fixture (default: 5).",
    )
    parser.add_argument(
        "--fixtures-dir",
        type=Path,
        default=ROOT / "tests" / "fixtures" / "benchmarks",
        help="Directory containing benchmark .md fixtures.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "tests" / "fixtures" / "benchmarks" / "warm_run_benchmark.json",
        help="Where to write the benchmark record.",
    )
    args = parser.parse_args()
    if args.iterations < 1:
        raise ValueError("--iterations must be >= 1")
    return args


def _safe_package_version(package_name: str) -> str | None:
    try:
        return metadata.version(package_name)
    except metadata.PackageNotFoundError:
        return None


def _size_payload(source: str) -> dict[str, int]:
    stripped = source.strip()
    paragraphs = 0 if not stripped else len([chunk for chunk in stripped.split("\n\n") if chunk.strip()])
    words = len(stripped.split()) if stripped else 0
    return {
        "chars": len(source),
        "lines": len(source.splitlines()),
        "paragraphs": paragraphs,
        "words": words,
    }


def _duration_payload(values_ms: list[float]) -> dict[str, object]:
    ordered = sorted(values_ms)
    p95_index = max(0, int(round((len(ordered) - 1) * 0.95)))
    return {
        "runs_ms": [round(value, 3) for value in values_ms],
        "mean": round(mean(values_ms), 3),
        "median": round(median(values_ms), 3),
        "min": round(min(values_ms), 3),
        "max": round(max(values_ms), 3),
        "p95": round(ordered[p95_index], 3),
    }


if __name__ == "__main__":
    main()
