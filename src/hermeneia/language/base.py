"""Language-pack contracts and shared settings."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping


@dataclass(frozen=True)
class PreprocessingPolicy:
    heavy_math_masking_ratio: float = 0.4
    symbol_dense_threshold: int = 4
    fragment_token_threshold: int = 4
    code_dominant_ratio: float = 0.5


@dataclass(frozen=True)
class LanguageLexicons:
    weak_support_verbs: frozenset[str] = frozenset()
    nominalization_suffixes: tuple[str, ...] = ()
    strong_claim_markers: tuple[str, ...] = ()
    contrast_markers: tuple[str, ...] = ()
    banned_transitions: tuple[str, ...] = ()
    acronym_allowlist: frozenset[str] = frozenset()
    definitional_markers: tuple[str, ...] = ()


@dataclass(frozen=True)
class LanguagePack:
    code: str
    name: str
    parser_model: str | None
    preprocessing: PreprocessingPolicy
    lexicons: LanguageLexicons
    rule_defaults: Mapping[str, Mapping[str, object]] = field(default_factory=dict)
    supported_rules: frozenset[str] = frozenset()
