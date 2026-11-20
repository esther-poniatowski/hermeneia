"""YAML configuration loading, and the location of the root and of the configuration file.

The root of a run is the folder from which Hermeneia finds its configuration file. The paths
written in that file and the paths of a SARIF log resolve against the root. Hodegos locates the
root and the file, as its specification states:
https://github.com/esther-poniatowski/hodegos/blob/main/docs/specification.md

The root is the first folder of this order:

- the option ``--root``;
- the folder named by the environment variable ``HERMENEIA_ROOT``;
- the nearest ancestor of the current folder holding the configuration file at one of its places;
- the current folder.

The configuration file ``hermeneia.yml`` lies at one of three places of the root: the root itself,
its subfolder ``.config/``, or its subfolder ``config/``. Two places holding the file are an error,
unless ``--config`` names another file. A file kept in any other folder is named by ``--config``.
"""

from __future__ import annotations

from pathlib import Path
from typing import Mapping

from hodegos import DiscoveryError, Tool, discover
import yaml

from hermeneia.config.schema import ConfigError, ProjectConfig, parse_project_config

TOOL = Tool("hermeneia", ("yml",))
"""Convention of Hermeneia for Hodegos: the file ``hermeneia.yml`` and the variable
``HERMENEIA_ROOT``."""


def discover_configuration(
    root: Path | None = None,
    config: Path | None = None,
    cwd: Path | None = None,
    environ: Mapping[str, str] | None = None,
) -> tuple[Path, Path | None]:
    """Return the root of a run and its configuration file, located through Hodegos.

    Parameters
    ----------
    root : Path | None
        Value of the option ``--root``, relative to the current folder. When None, Hodegos takes
        the root from ``HERMENEIA_ROOT`` or searches for it.
    config : Path | None
        Value of the option ``--config``, relative to the current folder.
    cwd : Path | None
        Current folder; the working directory of the process when absent.
    environ : Mapping[str, str] | None
        Environment variables; those of the process when absent.

    Returns
    -------
    tuple[Path, Path | None]
        The resolved root, and the configuration file. The file is ``config`` when named, else the
        single place of the root holding ``hermeneia.yml``. A root without the file at any place
        gives None, and the built-in defaults apply.

    Raises
    ------
    ConfigError
        If Hodegos rejects the request, or if the root names no folder. Hodegos rejects a named
        file that does not exist, and two places holding the file.
    """
    try:
        found = discover(TOOL, root=root, config=config, cwd=cwd, environ=environ)
    except DiscoveryError as error:
        raise ConfigError(str(error)) from error
    if not found.root.is_dir():
        raise ConfigError(f"the root {found.root} names no folder")
    path = found.configuration.path if found.configuration is not None else None
    return found.root.resolve(), path


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
