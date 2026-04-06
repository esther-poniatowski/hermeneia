"""Pytest configuration and shared fixtures for hermeneia tests."""

from __future__ import annotations

from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from hermeneia.config.profile import ProfileResolver
from hermeneia.config.schema import ProjectConfig
from hermeneia.engine.registry import RuleRegistry
from hermeneia.language.registry import LanguageRegistry
from hermeneia.rules.loader import load_builtin_rules


@pytest.fixture()
def registry() -> RuleRegistry:
    registry = RuleRegistry()
    load_builtin_rules(registry)
    return registry


@pytest.fixture()
def language_pack():
    return LanguageRegistry().get("en")


@pytest.fixture()
def research_profile(registry, language_pack):
    return ProfileResolver(registry).resolve(ProjectConfig(), language_pack)
