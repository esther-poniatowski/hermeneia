"""Tests of the resolution of the root and of the place of the settings file."""

from __future__ import annotations

from pathlib import Path

import pytest

from hermeneia.config.loader import find_settings, resolve_root
from hermeneia.config.schema import ConfigError


def _settings(folder: Path, place: str = "hermeneia.yml") -> Path:
    path = folder / place
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("{}\n", encoding="utf-8")
    return path


def test_option_wins_over_the_variable_and_the_search(tmp_path: Path) -> None:
    _settings(tmp_path)
    chosen = tmp_path / "chosen"
    chosen.mkdir()
    assert resolve_root(chosen, tmp_path, {"HERMENEIA_ROOT": str(tmp_path)}) == chosen.resolve()


def test_variable_wins_over_the_search_and_resolves_from_the_current_folder(
    tmp_path: Path,
) -> None:
    _settings(tmp_path)
    (tmp_path / "other").mkdir()
    assert resolve_root(None, tmp_path, {"HERMENEIA_ROOT": "other"}) == (tmp_path / "other")


def test_variable_naming_no_folder_is_an_error(tmp_path: Path) -> None:
    with pytest.raises(ConfigError, match="HERMENEIA_ROOT"):
        resolve_root(None, tmp_path, {"HERMENEIA_ROOT": "absent"})


@pytest.mark.parametrize("place", ["hermeneia.yml", "config/tools/hermeneia.yml"])
def test_search_finds_the_nearest_ancestor_holding_the_settings_file(
    tmp_path: Path, place: str
) -> None:
    _settings(tmp_path, place)
    nested = tmp_path / "notes" / "deep"
    nested.mkdir(parents=True)
    assert resolve_root(None, nested, {}) == tmp_path.resolve()


def test_search_ignores_a_former_name(tmp_path: Path) -> None:
    _settings(tmp_path, ".hermeneia.yaml")
    nested = tmp_path / "notes"
    nested.mkdir()
    assert resolve_root(None, nested, {}) == nested.resolve()


def test_current_folder_is_the_root_without_settings_file(tmp_path: Path) -> None:
    assert resolve_root(None, tmp_path, {}) == tmp_path.resolve()


def test_settings_file_is_read_from_either_place(tmp_path: Path) -> None:
    assert find_settings(tmp_path) is None
    tools = _settings(tmp_path, "config/tools/hermeneia.yml")
    assert find_settings(tmp_path) == tools


def test_two_settings_files_are_an_error_naming_both(tmp_path: Path) -> None:
    tools = _settings(tmp_path, "config/tools/hermeneia.yml")
    top = _settings(tmp_path)
    with pytest.raises(ConfigError) as error:
        find_settings(tmp_path)
    assert str(tools) in str(error.value) and str(top) in str(error.value)
