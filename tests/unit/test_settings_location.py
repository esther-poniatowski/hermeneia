"""Tests of how Hodegos locates the root of a run and its configuration file.

The root is the option ``--root``, else ``HERMENEIA_ROOT``, else the nearest ancestor of the
current folder holding ``hermeneia.yml`` at one of its places, else the current folder. The places
are the root, its ``.config/`` and its ``config/``; no other folder is searched. Two places holding
the file are an error. Hodegos reads a named ``--config`` from the current folder. Without a file
at any place, the built-in defaults apply.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from hermeneia.config.loader import discover_configuration
from hermeneia.config.schema import ConfigError

CONFIG = "config/hermeneia.yml"
"""Place of the configuration file in the subfolder ``config/`` of the root."""
UNSEARCHED = "shared/hermeneia.yml"
"""Configuration file in a folder that no place admits."""


def _write(folder: Path, place: str = "hermeneia.yml", content: str = "{}\n") -> Path:
    path = folder / place
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def test_option_wins_over_the_variable_and_the_search(tmp_path: Path) -> None:
    _write(tmp_path)
    chosen = tmp_path / "chosen"
    chosen.mkdir()
    root, path = discover_configuration(chosen, None, tmp_path, {"HERMENEIA_ROOT": str(tmp_path)})
    assert (root, path) == (chosen.resolve(), None)


def test_variable_wins_over_the_search_and_resolves_from_the_current_folder(
    tmp_path: Path,
) -> None:
    _write(tmp_path)
    settings = _write(tmp_path / "other")
    root, path = discover_configuration(None, None, tmp_path, {"HERMENEIA_ROOT": "other"})
    assert (root, path) == ((tmp_path / "other").resolve(), settings)


def test_root_naming_no_folder_is_an_error(tmp_path: Path) -> None:
    with pytest.raises(ConfigError, match="names no folder"):
        discover_configuration(None, None, tmp_path, {"HERMENEIA_ROOT": "absent"})
    with pytest.raises(ConfigError, match="names no folder"):
        discover_configuration(tmp_path / "absent", None, tmp_path, {})


@pytest.mark.parametrize("place", ["hermeneia.yml", ".config/hermeneia.yml", CONFIG])
def test_search_finds_the_nearest_ancestor_holding_the_file_at_one_of_its_places(
    tmp_path: Path, place: str
) -> None:
    settings = _write(tmp_path, place)
    nested = tmp_path / "notes" / "deep"
    nested.mkdir(parents=True)
    assert discover_configuration(None, None, nested, {}) == (tmp_path.resolve(), settings)


def test_search_ignores_a_folder_outside_the_places(tmp_path: Path) -> None:
    _write(tmp_path, UNSEARCHED)
    nested = tmp_path / "notes"
    nested.mkdir()
    assert discover_configuration(None, None, nested, {}) == (nested.resolve(), None)
    assert discover_configuration(tmp_path, None, tmp_path, {}) == (tmp_path.resolve(), None)


def test_search_ignores_a_former_name(tmp_path: Path) -> None:
    _write(tmp_path, ".hermeneia.yaml")
    nested = tmp_path / "notes"
    nested.mkdir()
    assert discover_configuration(None, None, nested, {}) == (nested.resolve(), None)


def test_current_folder_is_the_root_without_configuration_file(tmp_path: Path) -> None:
    assert discover_configuration(None, None, tmp_path, {}) == (tmp_path.resolve(), None)


def test_two_places_holding_the_file_are_an_error_naming_both(tmp_path: Path) -> None:
    config = _write(tmp_path, CONFIG)
    top = _write(tmp_path)
    with pytest.raises(ConfigError) as error:
        discover_configuration(tmp_path, None, tmp_path, {})
    assert str(config) in str(error.value) and str(top) in str(error.value)


def test_named_config_is_read_from_the_current_folder(tmp_path: Path) -> None:
    _write(tmp_path)
    other = _write(tmp_path / "settings", "other.yml")
    root, path = discover_configuration(tmp_path, Path("other.yml"), tmp_path / "settings", {})
    assert (root, path) == (tmp_path.resolve(), other)


def test_named_config_outside_the_places_leaves_the_current_folder_as_root(
    tmp_path: Path,
) -> None:
    named = _write(tmp_path, UNSEARCHED)
    root, path = discover_configuration(None, Path(UNSEARCHED), tmp_path, {})
    assert (root, path) == (tmp_path.resolve(), named)


def test_named_absent_config_is_an_error(tmp_path: Path) -> None:
    _write(tmp_path)
    with pytest.raises(ConfigError, match="absent.yml"):
        discover_configuration(tmp_path, Path("absent.yml"), tmp_path, {})
