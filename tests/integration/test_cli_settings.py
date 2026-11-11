"""Integration tests of the reserved options: root, configuration file and version."""

from __future__ import annotations

from pathlib import Path

import pytest
from typer.testing import CliRunner

from hermeneia import __version__
from hermeneia.cli import app

CONTRACTION = "The bound doesn't hold.\n"


def test_version_has_the_short_form() -> None:
    result = CliRunner().invoke(app, ["-v"])
    assert result.exit_code == 0
    assert result.stdout.strip() == __version__


def test_absent_settings_file_named_by_config_is_a_usage_error(tmp_path: Path) -> None:
    note = tmp_path / "note.md"
    note.write_text(CONTRACTION, encoding="utf-8")
    result = CliRunner().invoke(app, ["lint", str(note), "-c", str(tmp_path / "absent.yml")])
    assert result.exit_code == 2


def test_two_settings_files_stop_the_run(tmp_path: Path) -> None:
    note = tmp_path / "note.md"
    note.write_text(CONTRACTION, encoding="utf-8")
    (tmp_path / "config" / "tools").mkdir(parents=True)
    (tmp_path / "config" / "tools" / "hermeneia.yml").write_text("{}\n", encoding="utf-8")
    (tmp_path / "hermeneia.yml").write_text("{}\n", encoding="utf-8")
    result = CliRunner().invoke(app, ["lint", str(note), "-r", str(tmp_path)])
    assert result.exit_code == 2
    assert "two configuration files" in result.output


def test_root_from_the_variable_selects_the_settings_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    note = tmp_path / "note.md"
    note.write_text(CONTRACTION, encoding="utf-8")
    (tmp_path / "hermeneia.yml").write_text("reporting:\n  format: json\n", encoding="utf-8")
    arguments = ["lint", str(note), "--rule", "vocabulary.contraction"]
    assert '"results"' not in CliRunner().invoke(app, arguments).stdout
    monkeypatch.setenv("HERMENEIA_ROOT", str(tmp_path))
    assert '"results"' in CliRunner().invoke(app, arguments).stdout
