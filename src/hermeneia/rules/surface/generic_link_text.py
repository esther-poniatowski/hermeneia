"""Generic link-text checks."""

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
from hermeneia.rules.patterns import normalize_phrases


class GenericLinkTextRule(SourcePatternRule):
    metadata = RuleMetadata(
        rule_id="surface.generic_link_text",
        label="Avoid generic citation-like markdown link text",
        layer=Layer.SURFACE_STYLE,
        tractability=Tractability.CLASS_A,
        kind=RuleKind.SOFT_HEURISTIC,
        default_severity=Severity.INFO,
        supported_languages=frozenset({"en"}),
        evidence_fields=("link_text",),
    )

    def check_source(self, lines, doc, ctx):
        _ = doc
        link_text_pattern = _compile_generic_link_text_pattern(
            tuple(ctx.language_pack.lexicons.generic_link_reference_labels)
        )
        violations: list[Violation] = []
        for line in lines:
            if any(kind.value == "code_block" for kind in line.container_kinds):
                continue
            probe = line_text_outside_excluded(line)
            match = link_text_pattern.search(probe)
            if match is None:
                continue
            link_text = match.group(0)
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    message=(
                        "Generic link text hides the reference role; use descriptive anchor text "
                        "that states what the reader should take from the reference."
                    ),
                    span=_match_span(line, match.start(), match.end()),
                    severity=self.settings.severity,
                    layer=self.metadata.layer,
                    evidence=RuleEvidence(features={"link_text": link_text}),
                    rewrite_tactics=(
                        "Replace label-only link text with a descriptive, claim-relevant phrase.",
                    ),
                )
            )
        return violations


def _compile_generic_link_text_pattern(labels: tuple[str, ...]) -> re.Pattern[str]:
    normalized_labels = normalize_phrases(labels)
    if not normalized_labels:
        return re.compile(r"(?!x)x")
    label_body = "|".join(re.escape(label) for label in normalized_labels)
    return re.compile(
        rf"\[(?:{label_body})\s*\([^\]]+\)\]\([^)]*\)",
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
    registry.add(GenericLinkTextRule)
