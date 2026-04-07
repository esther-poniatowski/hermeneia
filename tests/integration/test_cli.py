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
    assert '"surface.contraction"' in result.stdout


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
                "surface.contraction",
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
