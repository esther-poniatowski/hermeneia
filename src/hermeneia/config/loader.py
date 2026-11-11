"""YAML configuration loading, and the location of the root and of the configuration file.

The root of a run is the folder from which Hermeneia finds its configuration file, and against which
the paths written in that file and the paths of a SARIF log resolve. It is resolved in this order:
the option ``--root``, the environment variable ``HERMENEIA_ROOT``, the nearest ancestor of the
current folder holding the configuration file, then the current folder. The configuration file is
``hermeneia.yml``, read from ``config/tools/hermeneia.yml`` or ``hermeneia.yml`` below the root.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Mapping

import yaml

from hermeneia.config.schema import ConfigError, ProjectConfig, parse_project_config

SETTINGS_NAME = "hermeneia.yml"
"""Name of the configuration file."""

SETTINGS_PLACES = (Path("config") / "tools" / SETTINGS_NAME, Path(SETTINGS_NAME))
"""Places of the configuration file below the root, in the order of the error naming both."""

ROOT_VARIABLE = "HERMENEIA_ROOT"
"""Environment variable naming the root when the option ``--root`` is absent."""


def resolve_root(
    option: Path | None,
    cwd: Path | None = None,
    environ: Mapping[str, str] | None = None,
) -> Path:
    """Return the root of a run.

    Parameters
    ----------
    option : Path | None
        Value of the option ``--root``, if given.
    cwd : Path | None
        Current folder; the working directory of the process when absent.
    environ : Mapping[str, str] | None
        Environment variables; those of the process when absent.

    Returns
    -------
    Path
        The option when given, else the folder named by ``HERMENEIA_ROOT``, else the nearest
        ancestor of the current folder holding a configuration file, else the current folder.

    Raises
    ------
    ConfigError
        If ``HERMENEIA_ROOT`` names no folder.
    """
    if option is not None:
        return option.resolve()
    environ = os.environ if environ is None else environ
    current = (cwd or Path.cwd()).resolve()
    variable = environ.get(ROOT_VARIABLE)
    if variable:
        root = (current / variable).resolve()
        if not root.is_dir():
            raise ConfigError(f"{ROOT_VARIABLE}={variable} names no folder")
        return root
    for candidate in (current, *current.parents):
        if any((candidate / place).is_file() for place in SETTINGS_PLACES):
            return candidate
    return current


def find_settings(root: Path) -> Path | None:
    """Return the configuration file below a root, or None when the root holds none.

    Raises
    ------
    ConfigError
        If both ``config/tools/hermeneia.yml`` and ``hermeneia.yml`` exist below the root.
    """
    found = [root / place for place in SETTINGS_PLACES if (root / place).is_file()]
    if len(found) > 1:
        raise ConfigError(
            f"two configuration files compete: {found[0]} and {found[1]}; keep only one of them"
        )
    return found[0] if found else None


def load_project_config(path: Path | None) -> ProjectConfig:
    """Load project config.

    Parameters
    ----------
    path : Path | None
        Path of the configuration file; the built-in defaults apply when absent.

    Returns
    -------
    ProjectConfig
        Resulting value produced by this call.
    """
    if path is None:
        return ProjectConfig()
    with path.open("r", encoding="utf-8") as handle:
        raw = yaml.safe_load(handle) or {}
    return parse_project_config(raw)
