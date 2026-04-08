"""Section-opener block-kind and framing checks."""

from __future__ import annotations

import re

from hermeneia.document.model import BlockKind
from hermeneia.rules.base import (
    HeuristicSemanticRule,
    Layer,
    RuleEvidence,
    RuleKind,
    RuleMetadata,
    Severity,
    Tractability,
    Violation,
)
from hermeneia.rules.patterns import compile_leading_phrase_regex

DEFINITION_OPENER_RE = re.compile(r"^\s*definition\b", re.IGNORECASE)


class SectionOpenerBlockKindRule(HeuristicSemanticRule):
    metadata = RuleMetadata(
        rule_id="structure.section_opener_block_kind",
        label="Section should open with purpose-oriented prose",
        layer=Layer.DOCUMENT_STRUCTURE,
        tractability=Tractability.CLASS_H,
        kind=RuleKind.RHETORICAL_EXPECTATION,
        default_severity=Severity.INFO,
        supported_languages=frozenset({"en"}),
        evidence_fields=("issue", "first_block_kind"),
    )

    def check(self, doc, ctx):
        definition_openers = tuple(ctx.language_pack.lexicons.definitional_markers) + (
            "definition",
        )
        definition_pattern = compile_leading_phrase_regex(definition_openers)
        violations: list[Violation] = []
        for section in ctx.features.sections:
            if section.heading_block_id is None or len(section.block_ids) < 2:
                continue
            first_content = doc.block_by_id(section.block_ids[1])
            heading = doc.block_by_id(section.heading_block_id)
            if first_content is None or heading is None:
                continue
            issue = _section_opening_issue(first_content, definition_pattern)
            if issue is None:
                continue
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    message=(
                        "Section opens without purpose-oriented prose; introduce the section "
                        "question or strategy before formal definitions or equations."
                    ),
                    span=first_content.span,
                    severity=self.settings.severity,
                    layer=self.metadata.layer,
                    evidence=RuleEvidence(
                        features={
                            "issue": issue,
                            "section_heading_id": heading.id,
                            "first_block_kind": first_content.kind.value,
                        }
                    ),
                    confidence=0.72,
                    rationale=(
                        "Section-opener checks inspect only the first content block for "
                        "high-signal opener patterns, not full rhetorical intent."
                    ),
                    rewrite_tactics=(
                        "Start the section with one prose sentence that states purpose before formal machinery.",
                    ),
                )
            )
        return violations


def _section_opening_issue(first_content, definition_pattern) -> str | None:
    if first_content.kind in {BlockKind.DISPLAY_MATH, BlockKind.CODE_BLOCK}:
        return "non_prose_opening"
    if first_content.kind != BlockKind.PARAGRAPH:
        return None
    if not first_content.sentences:
        return None
    opening_text = first_content.sentences[0].source_text.strip()
    if not opening_text:
        return None
    if DEFINITION_OPENER_RE.search(opening_text):
        return "definition_opening"
    if definition_pattern.search(opening_text):
        return "definitional_marker_opening"
    return None


def register(registry) -> None:
    registry.add(SectionOpenerBlockKindRule)

