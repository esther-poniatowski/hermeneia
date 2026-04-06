"""Rule-domain types and base classes."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any, ClassVar, Mapping

from hermeneia.document.indexes import FeatureStore
from hermeneia.document.model import Document, SourceLine, Span
from hermeneia.language.base import LanguagePack


class Layer(StrEnum):
    SURFACE_STYLE = "surface_style"
    LOCAL_DISCOURSE = "local_discourse"
    PARAGRAPH_RHETORIC = "paragraph_rhetoric"
    DOCUMENT_STRUCTURE = "document_structure"
    AUDIENCE_FIT = "audience_fit"


class Tractability(StrEnum):
    CLASS_A = "class_a"
    CLASS_B = "class_b"
    CLASS_H = "class_h"
    CLASS_C = "class_c"


class Severity(StrEnum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


class RuleKind(StrEnum):
    HARD_CONSTRAINT = "hard_constraint"
    SOFT_HEURISTIC = "soft_heuristic"
    DIAGNOSTIC_METRIC = "diagnostic_metric"
    RHETORICAL_EXPECTATION = "rhetorical_expectation"
    REWRITE_TACTIC = "rewrite_tactic"


@dataclass(frozen=True)
class RuleMetadata:
    rule_id: str
    label: str
    layer: Layer
    tractability: Tractability
    kind: RuleKind
    default_severity: Severity
    supported_languages: frozenset[str]
    default_weight: float = 1.0
    default_options: Mapping[str, object] = field(default_factory=dict)
    experimental: bool = False


@dataclass(frozen=True)
class RuleEvidence:
    features: Mapping[str, Any]
    score: float | None = None
    threshold: float | None = None
    upstream_limits: tuple[str, ...] = ()


@dataclass(frozen=True)
class Violation:
    rule_id: str
    message: str
    span: Span
    severity: Severity
    layer: Layer
    evidence: RuleEvidence | None = None
    confidence: float | None = None
    rationale: str | None = None
    rewrite_tactics: tuple[str, ...] = ()


@dataclass(frozen=True)
class ResolvedRuleSettings:
    metadata: RuleMetadata
    enabled: bool
    severity: Severity
    weight: float
    options: Mapping[str, object] = field(default_factory=dict)
    extra_patterns: tuple[str, ...] = ()
    silenced_patterns: tuple[str, ...] = ()

    def int_option(self, key: str, default: int) -> int:
        value = self.options.get(key, default)
        if isinstance(value, bool) or not isinstance(value, (int, float, str)):
            raise ValueError(f"Rule option '{key}' must be convertible to int")
        return int(value)

    def float_option(self, key: str, default: float) -> float:
        value = self.options.get(key, default)
        if isinstance(value, bool) or not isinstance(value, (int, float, str)):
            raise ValueError(f"Rule option '{key}' must be convertible to float")
        return float(value)


@dataclass(frozen=True)
class ResolvedProfile:
    profile_name: str
    audience: str
    genre: str
    section: str
    register: str
    language: str
    strict_validation: bool
    enable_experimental: bool
    rules: Mapping[str, ResolvedRuleSettings]

    def active_rules(self) -> tuple[ResolvedRuleSettings, ...]:
        return tuple(settings for settings in self.rules.values() if settings.enabled)


@dataclass(frozen=True)
class RuleContext:
    profile: ResolvedProfile
    language_pack: LanguagePack
    features: FeatureStore
    enable_experimental: bool = False


class BaseRule(ABC):
    metadata: ClassVar[RuleMetadata]

    def __init__(self, settings: ResolvedRuleSettings) -> None:
        self.settings = settings

    @property
    def rule_id(self) -> str:
        return self.metadata.rule_id

    @abstractmethod
    def check(self, doc: Document, ctx: RuleContext) -> list[Violation]: ...


class SourcePatternRule(BaseRule):
    @abstractmethod
    def check_source(
        self,
        lines: list[SourceLine],
        doc: Document,
        ctx: RuleContext,
    ) -> list[Violation]: ...

    def check(self, doc: Document, ctx: RuleContext) -> list[Violation]:
        return self.check_source(doc.source_lines, doc, ctx)


class AnnotatedRule(BaseRule):
    pass


class HeuristicSemanticRule(BaseRule):
    pass
