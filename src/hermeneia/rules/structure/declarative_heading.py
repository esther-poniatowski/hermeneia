"""Detect non-declarative heading forms."""

from __future__ import annotations

import re
from typing import Mapping

from hermeneia.document.model import BlockKind
from hermeneia.rules.base import (
    AnnotatedRule,
    Layer,
    RuleEvidence,
    RuleKind,
    RuleMetadata,
    Severity,
    Tractability,
    Violation,
)
from hermeneia.rules.patterns import normalize_phrases

COMMA_SEPARATOR = ", "
HEADING_START_RE = re.compile(r"^\s*(?P<first>[A-Za-z][A-Za-z-]*)")


class _DeclarativeHeadingOptions:
    """Declarativeheadingoptions."""

    def __init__(
        self,
        *,
        apply_heading_levels: tuple[int, ...] | None = None,
        forbid_question_headings: bool | None = None,
        forbid_imperative_headings: bool | None = None,
        imperative_verbs: tuple[str, ...] | None = None,
    ) -> None:
        """Initialize the instance."""
        self.apply_heading_levels = apply_heading_levels
        self.forbid_question_headings = forbid_question_headings
        self.forbid_imperative_headings = forbid_imperative_headings
        self.imperative_verbs = imperative_verbs

    @classmethod
    def model_validate(cls, raw: object) -> "_DeclarativeHeadingOptions":
        """Validate."""
        if not isinstance(raw, Mapping):
            raise ValueError("options must be a mapping")
        allowed = frozenset(
            {
                "apply_heading_levels",
                "forbid_question_headings",
                "forbid_imperative_headings",
                "imperative_verbs",
            }
        )
        unknown = sorted(key for key in raw if key not in allowed)
        if unknown:
            raise ValueError(f"unknown option keys: {COMMA_SEPARATOR.join(unknown)}")
        return cls(
            apply_heading_levels=_parse_heading_levels(raw.get("apply_heading_levels")),
            forbid_question_headings=_as_bool(
                raw.get("forbid_question_headings"), "forbid_question_headings"
            ),
            forbid_imperative_headings=_as_bool(
                raw.get("forbid_imperative_headings"),
                "forbid_imperative_headings",
            ),
            imperative_verbs=_as_string_tuple(raw.get("imperative_verbs"), "imperative_verbs"),
        )

    def model_dump(self) -> dict[str, object]:
        """Model dump."""
        dumped: dict[str, object] = {}
        if self.apply_heading_levels is not None:
            dumped["apply_heading_levels"] = self.apply_heading_levels
        if self.forbid_question_headings is not None:
            dumped["forbid_question_headings"] = self.forbid_question_headings
        if self.forbid_imperative_headings is not None:
            dumped["forbid_imperative_headings"] = self.forbid_imperative_headings
        if self.imperative_verbs is not None:
            dumped["imperative_verbs"] = self.imperative_verbs
        return dumped


class DeclarativeHeadingRule(AnnotatedRule):
    """Declarativeheadingrule."""

    options_model = _DeclarativeHeadingOptions

    metadata = RuleMetadata(
        rule_id="structure.declarative_heading",
        label="Headings should state a declarative deliverable",
        layer=Layer.DOCUMENT_STRUCTURE,
        tractability=Tractability.CLASS_A,
        kind=RuleKind.SOFT_HEURISTIC,
        default_severity=Severity.WARNING,
        supported_languages=frozenset({"en"}),
        default_options={
            "forbid_question_headings": True,
            "forbid_imperative_headings": True,
            "imperative_verbs": (
                "define",
                "assume",
                "let",
                "fix",
                "set",
                "check",
                "show",
                "prove",
                "consider",
                "use",
                "apply",
                "derive",
            ),
        },
        evidence_fields=("issue", "heading_text"),
    )

    def check(self, doc, ctx):
        """Check."""
        apply_levels = _resolve_heading_levels(self.settings.options.get("apply_heading_levels"))
        forbid_question = self.settings.bool_option("forbid_question_headings", True)
        forbid_imperative = self.settings.bool_option("forbid_imperative_headings", True)
        configured_imperative_verbs = _as_string_tuple(
            self.settings.options.get("imperative_verbs"), "imperative_verbs"
        )
        imperative_verbs = normalize_phrases(
            configured_imperative_verbs
            if configured_imperative_verbs is not None
            else tuple(ctx.language_pack.lexicons.imperative_opening_verbs)
        )
        violations: list[Violation] = []
        for block in doc.iter_blocks():
            if block.kind != BlockKind.HEADING:
                continue
            level = int(block.metadata.get("level", 1))
            if apply_levels is not None and level not in apply_levels:
                continue
            heading_text = " ".join(
                sentence.projection.text for sentence in block.sentences
            ).strip()
            if not heading_text:
                continue
            issue = _heading_issue(
                heading_text,
                forbid_question=forbid_question,
                forbid_imperative=forbid_imperative,
                imperative_verbs=imperative_verbs,
            )
            if issue is None:
                continue
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    message=(
                        "Heading should be declarative and content-bearing rather than interrogative or imperative."
                    ),
                    span=block.span,
                    severity=self.settings.severity,
                    layer=self.metadata.layer,
                    evidence=RuleEvidence(
                        features={"issue": issue, "heading_text": heading_text.lower()}
                    ),
                    rewrite_tactics=("Rewrite the heading to state what the section delivers.",),
                )
            )
        return violations


def _heading_issue(
    text: str,
    *,
    forbid_question: bool,
    forbid_imperative: bool,
    imperative_verbs: tuple[str, ...],
) -> str | None:
    """Heading issue."""
    if forbid_question and text.rstrip().endswith("?"):
        return "question_heading"
    if not forbid_imperative:
        return None
    first_word_match = HEADING_START_RE.match(text)
    if first_word_match is None:
        return None
    first = first_word_match.group("first").lower()
    if first in imperative_verbs:
        return "imperative_heading"
    return None


def _parse_heading_levels(raw: object) -> tuple[int, ...] | None:
    """Parse heading levels."""
    if raw is None:
        return None
    values: tuple[object, ...]
    if isinstance(raw, int):
        values = (raw,)
    elif isinstance(raw, (list, tuple)):
        values = tuple(raw)
    else:
        raise ValueError("apply_heading_levels must be an integer or sequence of integers")
    parsed: list[int] = []
    for value in values:
        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError("apply_heading_levels must be an integer or sequence of integers")
        if value < 1:
            raise ValueError("apply_heading_levels must contain values >= 1")
        parsed.append(value)
    return tuple(dict.fromkeys(parsed))


def _resolve_heading_levels(raw: object) -> frozenset[int] | None:
    """Resolve heading levels."""
    parsed = _parse_heading_levels(raw)
    if parsed is None:
        return None
    return frozenset(parsed)


def _as_bool(raw: object, field: str) -> bool | None:
    """As bool."""
    if raw is None:
        return None
    if isinstance(raw, bool):
        return raw
    raise ValueError(f"{field} must be a boolean")


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


def register(registry) -> None:
    """Register."""
    registry.add(DeclarativeHeadingRule)
