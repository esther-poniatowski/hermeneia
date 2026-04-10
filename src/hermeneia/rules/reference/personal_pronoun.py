"""Hard rule for first/second-person pronoun scaffolding."""

from __future__ import annotations

from hermeneia.document.model import BlockKind, Span
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
from hermeneia.rules.patterns import compile_inline_phrase_regex

PROSE_BLOCK_KINDS = {
    BlockKind.HEADING,
    BlockKind.PARAGRAPH,
    BlockKind.LIST_ITEM,
    BlockKind.BLOCK_QUOTE,
    BlockKind.TABLE_CELL,
    BlockKind.FOOTNOTE,
    BlockKind.ADMONITION,
}


class PersonalPronounRule(SourcePatternRule):
    metadata = RuleMetadata(
        rule_id="reference.personal_pronoun",
        label="Avoid first/second-person pronouns in technical prose",
        layer=Layer.SURFACE_STYLE,
        tractability=Tractability.CLASS_A,
        kind=RuleKind.HARD_CONSTRAINT,
        default_severity=Severity.ERROR,
        supported_languages=frozenset({"en"}),
        evidence_fields=("pronoun",),
    )

    def check_source(self, lines, doc, ctx):
        _ = doc
        pattern = compile_inline_phrase_regex(tuple(ctx.language_pack.lexicons.personal_pronoun_markers))
        if pattern.pattern == r"(?!x)x":
            return []
        violations: list[Violation] = []
        for line in lines:
            if not _is_prose_line(line):
                continue
            probe = line_text_outside_excluded(line)
            for match in pattern.finditer(probe):
                pronoun = match.group(0).lower()
                violations.append(
                    Violation(
                        rule_id=self.rule_id,
                        message=(
                            f"Replace first/second-person pronoun '{pronoun}' with "
                            "object-centered phrasing."
                        ),
                        span=_match_span(line, match.start(), match.end()),
                        severity=self.settings.severity,
                        layer=self.metadata.layer,
                        evidence=RuleEvidence(features={"pronoun": pronoun}),
                        rewrite_tactics=(
                            "Name the object, claim, operation, or result directly instead of addressing the reader or writer.",
                        ),
                    )
                )
        return violations


def _is_prose_line(line) -> bool:
    if not line.container_kinds:
        return True
    if any(kind in {BlockKind.CODE_BLOCK, BlockKind.DISPLAY_MATH} for kind in line.container_kinds):
        return False
    return any(kind in PROSE_BLOCK_KINDS for kind in line.container_kinds)


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
    registry.add(PersonalPronounRule)
