from __future__ import annotations

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
