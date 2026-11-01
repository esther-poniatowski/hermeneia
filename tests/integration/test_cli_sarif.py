from __future__ import annotations

import json
import sys

from typer.testing import CliRunner

from hermeneia.cli import app


def _log(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_cli_lint_writes_a_sarif_log(tmp_path) -> None:
    source = tmp_path / "notes" / "sample.md"
    source.parent.mkdir()
    source.write_text("It's obvious.\n", encoding="utf-8")
    output = tmp_path / "build" / "hermeneia.sarif"
    result = CliRunner().invoke(
        app,
        [
            "lint",
            str(source),
            "--format",
            "sarif",
            "--output",
            str(output),
            "--root",
            str(tmp_path),
            "--rule",
            "vocabulary.contraction",
        ],
    )
    assert result.exit_code == 0, result.output
    run = _log(output)["runs"][0]
    assert run["tool"]["driver"]["name"] == "hermeneia"
    assert "vocabulary.contraction" in {rule["id"] for rule in run["tool"]["driver"]["rules"]}
    assert run["invocations"] == [{"executionSuccessful": True}]
    assert run["columnKind"] == "unicodeCodePoints"
    (finding,) = run["results"]
    assert finding["ruleId"] == "vocabulary.contraction"
    assert finding["level"] == "warning"
    location = finding["locations"][0]
    assert location["physicalLocation"]["artifactLocation"] == {
        "uri": "notes/sample.md",
        "uriBaseId": "SRCROOT",
    }
    assert location["logicalLocations"] == [{"name": "path:notes/sample.md"}]
    assert finding["partialFingerprints"]["discriminator/v1"] == "[It's] It's obvious."
    assert "suppressions" not in finding and "fingerprints" not in finding


def test_cli_lint_declares_an_incomplete_run_on_a_rule_failure(tmp_path) -> None:
    module_path = tmp_path / "broken_sarif_module.py"
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
    source = tmp_path / "sample.md"
    source.write_text("A plain sentence.\n", encoding="utf-8")
    output = tmp_path / "hermeneia.sarif"
    sys.path.insert(0, str(tmp_path))
    try:
        result = CliRunner().invoke(
            app,
            [
                "lint",
                str(source),
                "--format",
                "sarif",
                "--output",
                str(output),
                "--root",
                str(tmp_path),
                "--rule",
                "test.broken",
                "--load-rules",
                "broken_sarif_module",
            ],
        )
    finally:
        sys.path.remove(str(tmp_path))
    assert result.exit_code == 0, result.output
    (invocation,) = _log(output)["runs"][0]["invocations"]
    assert invocation["executionSuccessful"] is False
    (notification,) = invocation["toolExecutionNotifications"]
    assert notification["level"] == "error"
    assert "rule_execution_error" in notification["message"]["text"]


def test_cli_lint_refuses_sarif_with_changed_and_output_without_sarif(tmp_path) -> None:
    source = tmp_path / "sample.md"
    source.write_text("A plain sentence.\n", encoding="utf-8")
    changed = CliRunner().invoke(app, ["lint", str(source), "--format", "sarif", "--changed"])
    assert changed.exit_code == 2
    assert "--changed" in changed.output
    stray = CliRunner().invoke(app, ["lint", str(source), "--output", str(tmp_path / "x")])
    assert stray.exit_code == 2
    assert "SARIF format" in changed.output or "SARIF format" in stray.output
