"""Detect document/tool subjects used as the main actor."""

from __future__ import annotations

import re

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


class ConcreteSubjectRule(SourcePatternRule):
    metadata = RuleMetadata(
        rule_id="surface.concrete_subject",
        label="Use concrete technical subjects instead of document/tool subjects",
        layer=Layer.SURFACE_STYLE,
        tractability=Tractability.CLASS_A,
        kind=RuleKind.HARD_CONSTRAINT,
        default_severity=Severity.ERROR,
        supported_languages=frozenset({"en"}),
        evidence_fields=("subject", "verb"),
    )

    def check_source(self, lines, doc, ctx):
        _ = doc
        subject_terms = tuple(ctx.language_pack.lexicons.concrete_subject_terms)
        action_verbs = tuple(ctx.language_pack.lexicons.concrete_subject_action_verbs)
        pattern = _compile_subject_pattern(subject_terms, action_verbs)
        if pattern is None:
            return []
        violations: list[Violation] = []
        for line in lines:
            if any(kind.value in {"code_block", "display_math"} for kind in line.container_kinds):
                continue
            probe = line_text_outside_excluded(line)
            match = pattern.search(probe)
            if match is None:
                continue
            subject = match.group("subject").lower()
            verb = match.group("verb").lower()
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    message=(
                        f"'{subject}' is used as the acting subject for '{verb}'; "
                        "name the mathematical object or result as subject."
                    ),
                    span=_match_span(line, match.start("subject"), match.end("verb")),
                    severity=self.settings.severity,
                    layer=self.metadata.layer,
                    evidence=RuleEvidence(features={"subject": subject, "verb": verb}),
                    rewrite_tactics=(
                        "Rewrite with the operative object/result as grammatical subject.",
                    ),
                )
            )
        return violations


def _compile_subject_pattern(
    subjects: tuple[str, ...],
    verbs: tuple[str, ...],
) -> re.Pattern[str] | None:
    normalized_subjects = tuple(sorted({item.strip().lower() for item in subjects if item.strip()}))
    normalized_verbs = tuple(sorted({item.strip().lower() for item in verbs if item.strip()}))
    if not normalized_subjects or not normalized_verbs:
        return None
    subject_body = "|".join(re.escape(item) for item in normalized_subjects)
    verb_body = "|".join(re.escape(item) for item in normalized_verbs)
    return re.compile(
        rf"^\s*(?P<subject>{subject_body})\b(?:\s+\w+){{0,4}}\s+(?P<verb>{verb_body})\b",
        re.IGNORECASE,
    )


def _match_span(line, start: int, end: int) -> Span:
    return Span(
        start=line.span.start + start,
        end=line.span.start + end,
        start_line=line.span.start_line,
        start_column=line.span.start_column + start,
        end_line=line.span.start_line,
        end_column=line.span.start_column + end,
    )


def register(registry) -> None:
    registry.add(ConcreteSubjectRule)
