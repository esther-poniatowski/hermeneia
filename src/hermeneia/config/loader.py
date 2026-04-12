"""YAML configuration loading."""

from __future__ import annotations

from pathlib import Path

import yaml

from hermeneia.config.schema import ProjectConfig, parse_project_config


def load_project_config(path: Path | None) -> ProjectConfig:
    """Load project config."""
    if path is None:
        return ProjectConfig()
    with path.open("r", encoding="utf-8") as handle:
        raw = yaml.safe_load(handle) or {}
    return parse_project_config(raw)
