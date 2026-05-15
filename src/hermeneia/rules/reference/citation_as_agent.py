"""Detect citation tags used as grammatical actors instead of tail evidence tags."""

from __future__ import annotations

import re
from typing import Mapping

from hermeneia.document.model import Span
from hermeneia.rules.base import (
    Layer,
    RuleEvidence,
    RuleKind,
    RuleMetadata,
    Severity,
    SourcePatternRule,
    Tractability,
    Violation,
)
from hermeneia.rules.common import line_text_outside_excluded
from hermeneia.rules.patterns import normalize_phrases
from hermeneia.rules.reference.citation_styles import (
    citation_union_pattern,
    resolve_citation_patterns,
)

COMMA_SEPARATOR = ", "


class _CitationAsAgentOptions:
    """Citationasagentoptions."""

    def __init__(
        self,
        *,
        citation_styles: tuple[str, ...] | None = None,
        citation_tag_pattern: str | None = None,
        citation_tag_patterns: tuple[str, ...] | None = None,
        agent_verbs: tuple[str, ...] | None = None,
        object_verbs: tuple[str, ...] | None = None,
        forbidden_prepositions: tuple[str, ...] | None = None,
        context_nouns: tuple[str, ...] | None = None,
    ) -> None:
        """Initialize the instance."""
        self.citation_styles = citation_styles
        self.citation_tag_pattern = citation_tag_pattern
        self.citation_tag_patterns = citation_tag_patterns
        self.agent_verbs = agent_verbs
        self.object_verbs = object_verbs
        self.forbidden_prepositions = forbidden_prepositions
        self.context_nouns = context_nouns

    @classmethod
    def model_validate(cls, raw: object) -> "_CitationAsAgentOptions":
        """Validate."""
        if not isinstance(raw, Mapping):
            raise ValueError("options must be a mapping")
        allowed = frozenset(
            {
                "citation_styles",
                "citation_tag_pattern",
                "citation_tag_patterns",
                "agent_verbs",
                "object_verbs",
                "forbidden_prepositions",
                "context_nouns",
            }
        )
        unknown = sorted(key for key in raw if key not in allowed)
        if unknown:
            raise ValueError(f"unknown option keys: {COMMA_SEPARATOR.join(unknown)}")
        pattern = raw.get("citation_tag_pattern")
        if pattern is not None and not isinstance(pattern, str):
            raise ValueError("citation_tag_pattern must be a string")
        citation_styles = _as_string_tuple(raw.get("citation_styles"), "citation_styles")
        citation_tag_patterns = _as_string_tuple(
            raw.get("citation_tag_patterns"), "citation_tag_patterns"
        )
        resolve_citation_patterns(
            citation_styles=citation_styles,
            citation_tag_pattern=pattern,
            citation_tag_patterns=citation_tag_patterns,
        )
        return cls(
            citation_styles=citation_styles,
            citation_tag_pattern=pattern,
            citation_tag_patterns=citation_tag_patterns,
            agent_verbs=_as_string_tuple(raw.get("agent_verbs"), "agent_verbs"),
            object_verbs=_as_string_tuple(raw.get("object_verbs"), "object_verbs"),
            forbidden_prepositions=_as_string_tuple(
                raw.get("forbidden_prepositions"), "forbidden_prepositions"
            ),
            context_nouns=_as_string_tuple(raw.get("context_nouns"), "context_nouns"),
        )

    def model_dump(self) -> dict[str, object]:
        """Model dump."""
        dumped: dict[str, object] = {}
        if self.citation_styles is not None:
            dumped["citation_styles"] = self.citation_styles
        if self.citation_tag_pattern is not None:
            dumped["citation_tag_pattern"] = self.citation_tag_pattern
        if self.citation_tag_patterns is not None:
            dumped["citation_tag_patterns"] = self.citation_tag_patterns
        if self.agent_verbs is not None:
            dumped["agent_verbs"] = self.agent_verbs
        if self.object_verbs is not None:
            dumped["object_verbs"] = self.object_verbs
        if self.forbidden_prepositions is not None:
            dumped["forbidden_prepositions"] = self.forbidden_prepositions
        if self.context_nouns is not None:
            dumped["context_nouns"] = self.context_nouns
        return dumped


class CitationAsAgentRule(SourcePatternRule):
    """Citationasagentrule."""

    options_model = _CitationAsAgentOptions

    metadata = RuleMetadata(
        rule_id="reference.citation_as_agent",
        label="Citation tags should not act as grammatical agents",
        layer=Layer.SURFACE_STYLE,
        tractability=Tractability.CLASS_A,
        kind=RuleKind.HARD_CONSTRAINT,
        default_severity=Severity.ERROR,
        supported_languages=frozenset({"en"}),
        default_options={"citation_styles": ("key_year_bracket",)},
        evidence_fields=("issue", "citation", "matched"),
    )

    def check_source(self, lines, doc, ctx):
        """Check source."""
        _ = doc
        citation_styles = _as_string_tuple(
            self.settings.options.get("citation_styles"),
            "citation_styles",
        )
        citation_tag_pattern_raw = self.settings.options.get("citation_tag_pattern")
        citation_tag_pattern = (
            str(citation_tag_pattern_raw).strip() if citation_tag_pattern_raw is not None else None
        )
        citation_tag_patterns = _as_string_tuple(
            self.settings.options.get("citation_tag_patterns"),
            "citation_tag_patterns",
        )
        citation_patterns = resolve_citation_patterns(
            citation_styles=citation_styles,
            citation_tag_pattern=citation_tag_pattern,
            citation_tag_patterns=citation_tag_patterns,
        )

        silenced = {value.lower() for value in self.settings.silenced_patterns}
        agent_verbs = _merged_terms(
            configured=_as_string_tuple(self.settings.options.get("agent_verbs"), "agent_verbs"),
            defaults=tuple(ctx.language_pack.lexicons.citation_agent_verbs),
            silenced=silenced,
        )
        object_verbs = _merged_terms(
            configured=_as_string_tuple(self.settings.options.get("object_verbs"), "object_verbs"),
            defaults=tuple(ctx.language_pack.lexicons.citation_object_verbs),
            silenced=silenced,
        )
        forbidden_prepositions = _merged_terms(
            configured=_as_string_tuple(
                self.settings.options.get("forbidden_prepositions"),
                "forbidden_prepositions",
            ),
            defaults=tuple(ctx.language_pack.lexicons.citation_forbidden_prepositions),
            silenced=silenced,
        )
        context_nouns = _merged_terms(
            configured=_as_string_tuple(
                self.settings.options.get("context_nouns"), "context_nouns"
            ),
            defaults=tuple(ctx.language_pack.lexicons.citation_context_nouns),
            silenced=silenced,
            extras=self.settings.extra_patterns,
        )

        patterns = _compiled_issue_patterns(
            citation_patterns=citation_patterns,
            agent_verbs=agent_verbs,
            object_verbs=object_verbs,
            forbidden_prepositions=forbidden_prepositions,
            context_nouns=context_nouns,
        )
        violations: list[Violation] = []
        seen_ranges: set[tuple[int, int]] = set()
        for line in lines:
            if any(kind.value in {"code_block", "display_math"} for kind in line.container_kinds):
                continue
            probe = line_text_outside_excluded(line)
            for issue, pattern in patterns:
                for match in pattern.finditer(probe):
                    span_key = (
                        line.span.start + match.start(),
                        line.span.start + match.end(),
                    )
                    if span_key in seen_ranges:
                        continue
                    seen_ranges.add(span_key)
                    citation = match.group("citation").lower()
                    matched = match.group(0).strip()
                    violations.append(
                        Violation(
                            rule_id=self.rule_id,
                            message=(
                                "Citations must support a statement as tail evidence, "
                                "not act as grammatical agents or containers."
                            ),
                            span=_match_span(line, match.start(), match.end()),
                            severity=self.settings.severity,
                            layer=self.metadata.layer,
                            evidence=RuleEvidence(
                                features={
                                    "issue": issue,
                                    "citation": citation,
                                    "matched": matched.lower(),
                                }
                            ),
                            rewrite_tactics=(
                                "State the result directly, then place the citation tag at the end of the statement.",
                            ),
                        )
                    )
        return violations


def _compiled_issue_patterns(
    *,
    citation_patterns: tuple[str, ...],
    agent_verbs: tuple[str, ...],
    object_verbs: tuple[str, ...],
    forbidden_prepositions: tuple[str, ...],
    context_nouns: tuple[str, ...],
) -> tuple[tuple[str, re.Pattern[str]], ...]:
    """Compile issue patterns."""
    citation_group = rf"(?P<citation>{citation_union_pattern(citation_patterns)})"
    compiled: list[tuple[str, re.Pattern[str]]] = []
    if agent_verbs:
        verb_body = "|".join(re.escape(value) for value in agent_verbs)
        compiled.append(
            (
                "citation_subject",
                re.compile(
                    rf"{citation_group}\s+(?P<lemma>{verb_body})\b",
                    re.IGNORECASE,
                ),
            )
        )
    compiled.append(
        (
            "citation_possessive",
            re.compile(rf"{citation_group}'s\b", re.IGNORECASE),
        )
    )
    if object_verbs:
        object_body = "|".join(re.escape(value) for value in object_verbs)
        compiled.append(
            (
                "citation_object",
                re.compile(
                    rf"\b(?P<lemma>{object_body})\s+(?:directly\s+)?{citation_group}",
                    re.IGNORECASE,
                ),
            )
        )
    if forbidden_prepositions:
        prep_body = "|".join(re.escape(value) for value in forbidden_prepositions)
        compiled.append(
            (
                "citation_preposition",
                re.compile(
                    rf"\b(?P<lemma>{prep_body})\s+(?:the\s+)?{citation_group}",
                    re.IGNORECASE,
                ),
            )
        )
    if context_nouns:
        noun_body = "|".join(re.escape(value) for value in context_nouns)
        compiled.append(
            (
                "citation_modifier",
                re.compile(rf"{citation_group}\s+(?P<lemma>{noun_body})\b", re.IGNORECASE),
            )
        )
    return tuple(compiled)


def _merged_terms(
    *,
    configured: tuple[str, ...] | None,
    defaults: tuple[str, ...],
    silenced: set[str],
    extras: tuple[str, ...] = (),
) -> tuple[str, ...]:
    """Merge configured/default terms with silencing and extras."""
    raw = configured if configured is not None else defaults
    normalized = normalize_phrases(tuple(raw) + tuple(extras))
    return tuple(value for value in normalized if value not in silenced)


def _as_string_tuple(raw: object, field: str) -> tuple[str, ...] | None:
    """As string tuple."""
    if raw is None:
        return None
    if isinstance(raw, str):
        return (raw,)
    if not isinstance(raw, (list, tuple)):
        raise ValueError(f"{field} must be a string or sequence of strings")
    if not all(isinstance(item, str) for item in raw):
        raise ValueError(f"{field} must be a string or sequence of strings")
    return tuple(raw)


def _match_span(line, start: int, end: int) -> Span:
    """Match span."""
    return Span(
        start=line.span.start + start,
        end=line.span.start + end,
        start_line=line.span.start_line,
        start_column=line.span.start_column + start,
        end_line=line.span.start_line,
        end_column=line.span.start_column + end,
    )


def register(registry) -> None:
    """Register."""
    registry.add(CitationAsAgentRule)
