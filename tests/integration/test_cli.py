from __future__ import annotations

import sys

from typer.testing import CliRunner

from hermeneia.cli import app


def test_cli_lint_reports_error_for_math_profile(tmp_path) -> None:
    path = tmp_path / "sample.md"
    path.write_text("Let $x$ be fixed.\n", encoding="utf-8")
    result = CliRunner().invoke(app, ["lint", str(path), "--profile", "math"])
    assert result.exit_code == 1
    assert "math.imperative_opening" in result.stdout


def test_cli_lint_json_output(tmp_path) -> None:
    path = tmp_path / "sample.md"
    path.write_text("It's obvious.\n", encoding="utf-8")
    result = CliRunner().invoke(
        app, ["lint", str(path), "--format", "json", "--fail-on", "warning"]
    )
    assert result.exit_code == 1
    assert '"vocabulary.contraction"' in result.stdout


def test_cli_lint_surfaces_rule_runtime_diagnostic(tmp_path) -> None:
    module_path = tmp_path / "broken_rule_module.py"
    module_path.write_text(
        "\n".join(
            [
                "from hermeneia.rules.base import Layer, RuleKind, RuleMetadata, Severity, SourcePatternRule, Tractability",
                "class BrokenRule(SourcePatternRule):",
                "    metadata = RuleMetadata(",
                "        rule_id='test.broken',",
                "        label='broken',",
                "        layer=Layer.SURFACE_STYLE,",
                "        tractability=Tractability.CLASS_A,",
                "        kind=RuleKind.SOFT_HEURISTIC,",
                "        default_severity=Severity.INFO,",
                "        supported_languages=frozenset({'en'}),",
                "    )",
                "    def check_source(self, lines, doc, ctx):",
                "        raise RuntimeError('synthetic rule failure')",
                "def register(registry):",
                "    registry.add(BrokenRule)",
            ]
        ),
        encoding="utf-8",
    )
    path = tmp_path / "sample.md"
    path.write_text("It's obvious.\n", encoding="utf-8")
    sys.path.insert(0, str(tmp_path))
    try:
        result = CliRunner().invoke(
            app,
            [
                "lint",
                str(path),
                "--format",
                "json",
                "--rule",
                "vocabulary.contraction",
                "--rule",
                "test.broken",
                "--load-rules",
                "broken_rule_module",
            ],
        )
    finally:
        sys.path.remove(str(tmp_path))
    assert result.exit_code == 0
    assert '"code": "rule_execution_error"' in result.stdout
    assert '"test.broken: synthetic rule failure"' in result.stdout


def test_cli_lint_renders_multiline_span_annotations(tmp_path) -> None:
    module_path = tmp_path / "multiline_rule_module.py"
    module_path.write_text(
        "\n".join(
            [
                "from hermeneia.document.model import Span",
                "from hermeneia.rules.base import Layer, RuleKind, RuleMetadata, Severity, SourcePatternRule, Tractability, Violation",
                "class MultiLineRule(SourcePatternRule):",
                "    metadata = RuleMetadata(",
                "        rule_id='test.multiline',",
                "        label='multiline',",
                "        layer=Layer.SURFACE_STYLE,",
                "        tractability=Tractability.CLASS_A,",
                "        kind=RuleKind.DIAGNOSTIC_METRIC,",
                "        default_severity=Severity.ERROR,",
                "        supported_languages=frozenset({'en'}),",
                "    )",
                "    def check_source(self, lines, doc, ctx):",
                "        _ = doc, ctx",
                "        if len(lines) < 2:",
                "            return []",
                "        span = Span(",
                "            start=lines[0].span.start + 6,",
                "            end=lines[1].span.start + 6,",
                "            start_line=1,",
                "            start_column=7,",
                "            end_line=2,",
                "            end_column=7,",
                "        )",
                "        return [Violation(",
                "            rule_id=self.rule_id,",
                "            message='multiline span',",
                "            span=span,",
                "            severity=self.settings.severity,",
                "            layer=self.metadata.layer,",
                "        )]",
                "def register(registry):",
                "    registry.add(MultiLineRule)",
            ]
        ),
        encoding="utf-8",
    )
    path = tmp_path / "sample.md"
    path.write_text("alpha beta\nsecond line\n", encoding="utf-8")
    sys.path.insert(0, str(tmp_path))
    try:
        result = CliRunner().invoke(
            app,
            [
                "lint",
                str(path),
                "--rule",
                "test.multiline",
                "--load-rules",
                "multiline_rule_module",
            ],
        )
    finally:
        sys.path.remove(str(tmp_path))
    assert result.exit_code == 1
    assert "1: alpha beta" in result.stdout
    assert "2: second line" in result.stdout
    assert "      ^^^^" in result.stdout
    assert "^^^^^^" in result.stdout


def test_cli_lint_text_output_includes_evidence_confidence_rationale(tmp_path) -> None:
    path = tmp_path / "sample.md"
    path.write_text("This clearly proves the theorem.\n", encoding="utf-8")
    result = CliRunner().invoke(
        app,
        [
            "lint",
            str(path),
            "--rule",
            "evidence.claim_calibration",
            "--fail-on",
            "info",
        ],
    )
    assert result.exit_code == 1
    assert "evidence.claim_calibration" in result.stdout
    assert "evidence.score=0.000" in result.stdout
    assert "evidence.threshold=1.000" in result.stdout
    assert "evidence.features=" in result.stdout
    assert '"claim_markers": [' in result.stdout
    assert '"clearly"' in result.stdout
    assert '"proves"' in result.stdout
    assert "confidence=0.700" in result.stdout
    assert "rationale=Claim calibration uses bounded evidence lookback" in result.stdout


def test_cli_lint_respects_scoring_output_config_in_json_report(tmp_path) -> None:
    path = tmp_path / "sample.md"
    path.write_text("It's obvious.\n", encoding="utf-8")
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "\n".join(
            [
                "rules:",
                "  active:",
                "    - vocabulary.contraction",
                "scoring:",
                "  output:",
                "    - violation_list",
                "reporting:",
                "  format: json",
            ]
        ),
        encoding="utf-8",
    )
    result = CliRunner().invoke(
        app,
        [
            "lint",
            str(path),
            "--config",
            str(config_path),
            "--fail-on",
            "warning",
        ],
    )
    assert result.exit_code == 1
    assert '"vocabulary.contraction"' in result.stdout
    assert '"scorecard"' not in result.stdout
    assert '"global_score"' not in result.stdout
    assert '"layer_scores"' not in result.stdout


def test_cli_lint_respects_suggestions_enabled_flag(tmp_path) -> None:
    path = tmp_path / "sample.md"
    path.write_text("It's obvious.\n", encoding="utf-8")
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "\n".join(
            [
                "rules:",
                "  active:",
                "    - vocabulary.contraction",
                "suggestions:",
                "  enabled: false",
                "reporting:",
                "  format: json",
            ]
        ),
        encoding="utf-8",
    )
    result = CliRunner().invoke(
        app,
        [
            "lint",
            str(path),
            "--config",
            str(config_path),
            "--fail-on",
            "warning",
        ],
    )
    assert result.exit_code == 1
    assert '"vocabulary.contraction"' in result.stdout
    assert '"revision_plan"' in result.stdout
    assert '"operations": []' in result.stdout
