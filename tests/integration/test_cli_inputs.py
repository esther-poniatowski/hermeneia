"""Integration tests of the inputs of the command line: changed lines, kinds, exclusions and terms.

Each test builds a small project in a temporary directory, with a git repository where the test
requires a repository, and runs ``hermeneia lint`` in compact format, one finding per line.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

from typer.testing import CliRunner

from hermeneia.cli import app

CONTRACTION = "The bound doesn't hold.\n"
CLEAN = "The bound holds for every gain.\n"


def _git(root: Path, *args: str) -> None:
    """Run a git command in a test repository, with a fixed identity."""
    subprocess.run(
        ["git", "-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false", *args],
        cwd=root,
        check=True,
        capture_output=True,
    )


def _lint(*args: str) -> list[str]:
    """Run the linter in compact format and return the reported rule ids."""
    result = CliRunner().invoke(app, ["lint", "--format", "compact", "--fail-on", "error", *args])
    assert result.exit_code in {0, 1}, result.output
    return [line.split()[2].rstrip(":") for line in result.stdout.splitlines() if line.strip()]


def test_changed_reports_only_the_changed_lines(tmp_path: Path) -> None:
    note = tmp_path / "note.md"
    note.write_text(CONTRACTION + "\n" + CLEAN, encoding="utf-8")
    _git(tmp_path, "init", "-q")
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-q", "-m", "base")
    note.write_text(CONTRACTION + "\n" + "The rate doesn't change.\n", encoding="utf-8")
    untracked = tmp_path / "new.md"
    untracked.write_text(CONTRACTION, encoding="utf-8")
    full = _lint(str(note), "--rule", "vocabulary.contraction")
    changed = _lint(str(tmp_path), "--changed", "--rule", "vocabulary.contraction")
    assert full.count("vocabulary.contraction") == 2
    # the unchanged first line of note.md is dropped; the untracked file counts in full
    assert changed.count("vocabulary.contraction") == 2


def test_directory_collects_the_declared_kinds_outside_excluded_dirs(tmp_path: Path) -> None:
    (tmp_path / "_backup").mkdir()
    (tmp_path / "_backup" / "old.md").write_text(CONTRACTION, encoding="utf-8")
    (tmp_path / "note.md").write_text(CONTRACTION, encoding="utf-8")
    (tmp_path / "settings.yaml").write_text(
        "# Capitalized comment doesn't fit.\nkey: 1\n", encoding="utf-8"
    )
    (tmp_path / ".hermeneia.yaml").write_text(
        "inputs:\n  kinds: [markdown, yaml]\n  exclude_dirs: [_backup]\n", encoding="utf-8"
    )
    found = _lint(str(tmp_path), "--rule", "vocabulary.contraction")
    assert found.count("vocabulary.contraction") == 2  # note.md and the YAML comment
    assert len(_lint(str(tmp_path), "--rule", "vocabulary.contraction", "--no-exclude")) == 3


def test_terminology_files_exempt_project_terms(tmp_path: Path) -> None:
    note = tmp_path / "note.md"
    note.write_text("The violation of the rule fails the run.\n", encoding="utf-8")
    assert "vocabulary.nominalization" in _lint(str(note), "--rule", "vocabulary.nominalization")
    (tmp_path / "terms.yml").write_text("terms:\n  v: {label: violation}\n", encoding="utf-8")
    (tmp_path / ".hermeneia.yaml").write_text(
        "terminology:\n  files:\n    - {path: terms.yml, select: terms.*.label}\n", encoding="utf-8"
    )
    assert "vocabulary.nominalization" not in _lint(
        str(note), "--rule", "vocabulary.nominalization"
    )


def test_several_targets_are_linted_together(tmp_path: Path) -> None:
    first, second = tmp_path / "a.md", tmp_path / "b.md"
    first.write_text(CONTRACTION, encoding="utf-8")
    second.write_text(CONTRACTION, encoding="utf-8")
    assert (
        _lint(str(first), str(second), "--rule", "vocabulary.contraction").count(
            "vocabulary.contraction"
        )
        == 2
    )


def test_frontmatter_keys_are_linted_on_their_lines(tmp_path: Path) -> None:
    note = tmp_path / "note.md"
    note.write_text(
        '---\npurpose: "fixes the rules of the vault."\n---\n# Note\n', encoding="utf-8"
    )
    assert "structure.field_form" not in _lint(str(note), "--rule", "structure.field_form")
    (tmp_path / ".hermeneia.yaml").write_text(
        "inputs:\n  frontmatter_keys: [purpose]\n"
        "rules:\n  overrides:\n    structure.field_form: {options: {forms: {purpose: gloss}}}\n",
        encoding="utf-8",
    )
    result = CliRunner().invoke(
        app, ["lint", "--format", "compact", "--rule", "structure.field_form", str(note)]
    )
    assert f"{note}:2: warning structure.field_form" in result.stdout
