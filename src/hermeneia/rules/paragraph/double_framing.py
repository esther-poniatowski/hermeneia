"""Detect double framing in list lead-ins and list items."""

from __future__ import annotations

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
from hermeneia.rules.common import text_has_marker


class DoubleFramingRule(HeuristicSemanticRule):
    metadata = RuleMetadata(
        rule_id="paragraph.double_framing",
        label="Avoid double framing around list introductions",
        layer=Layer.PARAGRAPH_RHETORIC,
        tractability=Tractability.CLASS_H,
        kind=RuleKind.SOFT_HEURISTIC,
        default_severity=Severity.WARNING,
        supported_languages=frozenset({"en"}),
        evidence_fields=("list_item_count", "reframed_item_count"),
    )

    def check(self, doc, ctx):
        framing_markers = tuple(ctx.language_pack.lexicons.list_framing_markers)
        flat_blocks = list(doc.iter_blocks())
        violations: list[Violation] = []
        for index, block in enumerate(flat_blocks):
            if block.kind not in {BlockKind.PARAGRAPH, BlockKind.BLOCK_QUOTE}:
                continue
            if not block.sentences:
                continue
            lead = block.sentences[-1].projection.text.strip().lower()
            if not lead.endswith(":"):
                continue
            if not text_has_marker(lead, framing_markers):
                continue
            list_items = _following_list_items(flat_blocks, index)
            if len(list_items) < 2:
                continue
            reframed = sum(
                1 for item in list_items if _item_reframes(item, framing_markers)
            )
            if reframed < 2:
                continue
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    message=(
                        "Lead-in and list items both re-frame content; keep framing in the lead-in "
                        "and make list items directly informative."
                    ),
                    span=block.span,
                    severity=self.settings.severity,
                    layer=self.metadata.layer,
                    evidence=RuleEvidence(
                        features={
                            "list_item_count": len(list_items),
                            "reframed_item_count": reframed,
                        }
                    ),
                    confidence=0.72,
                    rationale=(
                        "Double-framing detection relies on local marker cues in lead-ins and "
                        "item openings."
                    ),
                    rewrite_tactics=(
                        "Keep one framing sentence before the list, and rewrite list items as direct claims.",
                    ),
                )
            )
        return violations


def _following_list_items(blocks, index: int):
    if index + 1 >= len(blocks):
        return []
    next_block = blocks[index + 1]
    if next_block.kind == BlockKind.LIST:
        return [item for item in next_block.children if item.kind == BlockKind.LIST_ITEM]
    if next_block.kind != BlockKind.LIST_ITEM:
        return []
    items = [next_block]
    cursor = index + 2
    while cursor < len(blocks) and blocks[cursor].kind == BlockKind.LIST_ITEM:
        items.append(blocks[cursor])
        cursor += 1
    return items


def _item_reframes(item, markers: tuple[str, ...]) -> bool:
    opening = _first_sentence_text(item)
    if opening is None:
        return False
    opening = opening.strip().lower()
    if not opening:
        return False
    if opening.startswith(("this ", "it ", "these ", "that ")):
        return True
    return text_has_marker(opening, markers)


def _first_sentence_text(block) -> str | None:
    if block.sentences:
        return block.sentences[0].projection.text
    for descendant in block.iter_blocks():
        if descendant is block:
            continue
        if descendant.sentences:
            return descendant.sentences[0].projection.text
    return None


def register(registry) -> None:
    registry.add(DoubleFramingRule)
