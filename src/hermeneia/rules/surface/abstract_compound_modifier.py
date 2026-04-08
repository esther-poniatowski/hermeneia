"""Detect abstract compound modifiers that hide explicit relations."""

from __future__ import annotations

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
from hermeneia.rules.patterns import compile_hyphen_suffix_regex


class AbstractCompoundModifierRule(SourcePatternRule):
    metadata = RuleMetadata(
        rule_id="surface.abstract_compound_modifier",
        label="Replace abstract compound modifiers with explicit relations",
        layer=Layer.SURFACE_STYLE,
        tractability=Tractability.CLASS_A,
        kind=RuleKind.SOFT_HEURISTIC,
        default_severity=Severity.INFO,
        supported_languages=frozenset({"en"}),
        evidence_fields=("compound",),
    )

    def check_source(self, lines, doc, ctx):
        _ = doc, ctx
        compound_pattern = compile_hyphen_suffix_regex(
            tuple(ctx.language_pack.lexicons.abstract_compound_suffixes)
        )
        violations: list[Violation] = []
        for line in lines:
            if any(kind.value in {"code_block"} for kind in line.container_kinds):
                continue
            probe = line_text_outside_excluded(line)
            match = compound_pattern.search(probe)
            if match is None:
                continue
            compound = match.group(0)
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    message=(
                        f"Compound modifier '{compound}' is abstract; state the dependency "
                        "or criterion explicitly."
                    ),
                    span=_match_span(line, match.start(), match.end()),
                    severity=self.settings.severity,
                    layer=self.metadata.layer,
                    evidence=RuleEvidence(features={"compound": compound.lower()}),
                    confidence=0.76,
                    rewrite_tactics=(
                        "Rewrite the compound as a clause that states what depends on what, and how.",
                    ),
                )
            )
        return violations


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
    registry.add(AbstractCompoundModifierRule)
