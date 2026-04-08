"""Consecutive display-block bridge checks."""

from __future__ import annotations

from hermeneia.document.model import BlockKind, Span
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
from hermeneia.rules.common import previous_prose_block, text_has_marker


class ConsecutiveDisplayBlocksWithoutBridgeRule(HeuristicSemanticRule):
    metadata = RuleMetadata(
        rule_id="math.consecutive_display_blocks_without_bridge",
        label="Consecutive display equations need a motivational bridge",
        layer=Layer.DOCUMENT_STRUCTURE,
        tractability=Tractability.CLASS_H,
        kind=RuleKind.RHETORICAL_EXPECTATION,
        default_severity=Severity.INFO,
        supported_languages=frozenset({"en"}),
        default_options={"min_chain_length": 2},
        evidence_fields=("chain_length", "has_preceding_motivation"),
    )

    def check(self, doc, ctx):
        min_chain_length = self.settings.int_option("min_chain_length", 2)
        motivation_markers = tuple(ctx.language_pack.lexicons.assumption_purpose_markers)
        motivation_action_verbs = tuple(ctx.language_pack.lexicons.motivation_action_verbs)
        flat_blocks = list(doc.iter_blocks())
        violations: list[Violation] = []
        index = 0
        while index < len(flat_blocks):
            if flat_blocks[index].kind != BlockKind.DISPLAY_MATH:
                index += 1
                continue
            chain_start = index
            chain_end = index
            while (
                chain_end + 1 < len(flat_blocks)
                and flat_blocks[chain_end + 1].kind == BlockKind.DISPLAY_MATH
            ):
                chain_end += 1
            chain_length = chain_end - chain_start + 1
            if chain_length >= min_chain_length:
                preceding = previous_prose_block(flat_blocks, chain_start)
                has_preceding_motivation = _has_preceding_motivation(
                    preceding,
                    motivation_markers,
                    motivation_action_verbs,
                )
                if not has_preceding_motivation:
                    span = _chain_span(flat_blocks[chain_start], flat_blocks[chain_end])
                    violations.append(
                        Violation(
                            rule_id=self.rule_id,
                            message=(
                                "Consecutive display equations appear without a preceding "
                                "motivational bridge."
                            ),
                            span=span,
                            severity=self.settings.severity,
                            layer=self.metadata.layer,
                            evidence=RuleEvidence(
                                features={
                                    "chain_length": chain_length,
                                    "has_preceding_motivation": has_preceding_motivation,
                                },
                                score=float(chain_length),
                                threshold=float(min_chain_length),
                            ),
                            confidence=0.66,
                            rationale=(
                                "Bridge checks detect local display-equation chains and do not "
                                "model deeper section-level narrative context."
                            ),
                            rewrite_tactics=(
                                "Add one motivation sentence before the chain that states the shared purpose of the introduced objects.",
                            ),
                        )
                    )
            index = chain_end + 1
        return violations


def _chain_span(first_block, last_block) -> Span:
    return Span(
        start=first_block.span.start,
        end=last_block.span.end,
        start_line=first_block.span.start_line,
        start_column=first_block.span.start_column,
        end_line=last_block.span.end_line,
        end_column=last_block.span.end_column,
    )


def _has_preceding_motivation(
    preceding,
    motivation_markers: tuple[str, ...],
    motivation_action_verbs: tuple[str, ...],
) -> bool:
    if preceding is None or not preceding.sentences:
        return False
    text = " ".join(sentence.projection.text for sentence in preceding.sentences).strip()
    if not text:
        return False
    if text_has_marker(text, motivation_markers):
        return True
    return text.endswith(":") and text_has_marker(text, motivation_action_verbs)


def register(registry) -> None:
    registry.add(ConsecutiveDisplayBlocksWithoutBridgeRule)
