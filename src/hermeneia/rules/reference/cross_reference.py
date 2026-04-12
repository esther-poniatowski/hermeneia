"""Ambiguous cross-reference checks."""

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
from hermeneia.rules.patterns import compile_inline_phrase_regex, normalize_phrases


class CrossReferenceRule(SourcePatternRule):
    """Crossreferencerule."""

    metadata = RuleMetadata(
        rule_id="reference.cross_reference",
        label="Cross-reference should target an explicit object",
        layer=Layer.SURFACE_STYLE,
        tractability=Tractability.CLASS_A,
        kind=RuleKind.SOFT_HEURISTIC,
        default_severity=Severity.INFO,
        supported_languages=frozenset({"en"}),
        evidence_fields=("reference",),
    )

    def check_source(self, lines, doc, ctx):
        """Check source."""
        _ = doc
        ambiguous_pattern = _compile_ambiguous_reference_pattern(
            tuple(ctx.language_pack.lexicons.ambiguous_reference_verbs),
            tuple(ctx.language_pack.lexicons.ambiguous_reference_positions),
        )
        explicit_target_pattern = compile_inline_phrase_regex(
            tuple(ctx.language_pack.lexicons.explicit_reference_targets)
        )
        violations: list[Violation] = []
        for line in lines:
            if any(
                kind.value in {"code_block", "display_math"}
                for kind in line.container_kinds
            ):
                continue
            probe = line_text_outside_excluded(line)
            match = ambiguous_pattern.search(probe)
            if match is None:
                continue
            if explicit_target_pattern.search(probe):
                continue
            reference = match.group(0).strip()
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    message=f"Reference '{reference}' is ambiguous; name the section, theorem, or equation explicitly.",
                    span=_match_span(line, match.start(), match.end()),
                    severity=self.settings.severity,
                    layer=self.metadata.layer,
                    evidence=RuleEvidence(features={"reference": reference.lower()}),
                    rewrite_tactics=(
                        "Replace positional references with explicit anchors (for example, Section 3 or Theorem 2).",
                    ),
                )
            )
        return violations


def _compile_ambiguous_reference_pattern(
    verbs: tuple[str, ...], positions: tuple[str, ...]
) -> re.Pattern[str]:
    """Compile ambiguous reference pattern."""
    normalized_positions = normalize_phrases(positions)
    if not normalized_positions:
        return re.compile(r"(?!x)x")
    normalized_verbs = normalize_phrases(verbs)
    position_body = "|".join(re.escape(item) for item in normalized_positions)
    if normalized_verbs:
        verb_body = "|".join(re.escape(item) for item in normalized_verbs)
        return re.compile(
            rf"\b(?:as\s+)?(?:{verb_body})?\s*(?:{position_body})\b",
            re.IGNORECASE,
        )
    return re.compile(rf"\b(?:as\s+)?(?:{position_body})\b", re.IGNORECASE)


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
    registry.add(CrossReferenceRule)
