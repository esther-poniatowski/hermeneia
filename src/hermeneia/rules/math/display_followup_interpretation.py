"""Post-display interpretation checks."""

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
from hermeneia.rules.common import matched_sentence_markers, sentence_word_count
from hermeneia.rules.patterns import compile_inline_phrase_regex

DISPLAY_OPERATOR_RE = re.compile(r"(?:=|\\frac|\\sum|\\int|\\to|\\Rightarrow|[+\-*/^])")
CONTENT_FREE_FOLLOWUP_RE = re.compile(
    r"^\s*(?:it|this|that)?\s*(?:follows|holds)\.?\s*$",
    re.IGNORECASE,
)
DEMONSTRATIVE_PREDICATE_RE = re.compile(
    r"^\s*(?:this|these)\s+"
    r"(?:is|are|was|were|can|could|may|might|must|should|would|will|"
    r"follows|follow|gives|give|shows|show|implies|imply|yields|yield|"
    r"means|mean|holds|hold|states|state|demonstrates|demonstrate|proves|prove)\b",
    re.IGNORECASE,
)
IT_THEY_OPENING_RE = re.compile(r"^\s*(?:it|they)\b", re.IGNORECASE)


class DisplayFollowupInterpretationRule(HeuristicSemanticRule):
    """Displayfollowupinterpretationrule."""

    metadata = RuleMetadata(
        rule_id="math.display_followup_interpretation",
        label="Display formulas should be followed by interpretive prose",
        layer=Layer.LOCAL_DISCOURSE,
        tractability=Tractability.CLASS_H,
        kind=RuleKind.RHETORICAL_EXPECTATION,
        default_severity=Severity.INFO,
        supported_languages=frozenset({"en"}),
        default_options={"min_display_chars": 12},
        evidence_fields=("issue",),
    )

    def check(self, doc, ctx):
        """Check."""
        min_display_chars = self.settings.int_option("min_display_chars", 12)
        interpretation_markers = tuple(
            ctx.language_pack.lexicons.formula_interpretation_markers
        )
        weak_transition_markers = frozenset(
            marker.lower()
            for marker in ctx.language_pack.lexicons.transition_connectors
        )
        interpretive_noun_pattern = compile_inline_phrase_regex(
            tuple(ctx.language_pack.lexicons.display_interpretive_nouns)
        )
        flat_blocks = list(doc.iter_blocks())
        violations: list[Violation] = []
        for index, block in enumerate(flat_blocks):
            if block.kind != BlockKind.DISPLAY_MATH:
                continue
            display_text = _display_text(doc, block)
            if not _is_nontrivial_display(display_text, min_display_chars):
                continue
            next_sentence = _next_followup_sentence(flat_blocks, index)
            if next_sentence is None:
                violations.append(
                    _build_violation(
                        self,
                        block,
                        issue="missing_followup_sentence",
                        score=None,
                        threshold=None,
                    )
                )
                continue
            if _is_interpretive_followup(
                next_sentence,
                interpretation_markers,
                weak_transition_markers,
                interpretive_noun_pattern,
            ):
                continue
            if _is_bare_pronoun_followup(next_sentence):
                # reference.bare_pronoun_opening handles this case explicitly.
                continue
            violations.append(
                _build_violation(
                    self,
                    next_sentence,
                    issue="missing_interpretive_followup",
                    score=0.0,
                    threshold=1.0,
                )
            )
        return violations


def _build_violation(
    rule, span_owner, issue: str, score: float | None, threshold: float | None
):
    """Build violation."""
    return Violation(
        rule_id=rule.rule_id,
        message=(
            "Display formula should be followed by an interpretive sentence naming "
            "its role, operation, or consequence."
        ),
        span=span_owner.span,
        severity=rule.settings.severity,
        layer=rule.metadata.layer,
        evidence=RuleEvidence(
            features={"issue": issue},
            score=score,
            threshold=threshold,
        ),
        confidence=0.64,
        rationale=(
            "Interpretation checks use local lexical cues and may miss deeply implicit "
            "commentary."
        ),
        rewrite_tactics=(
            "Add one sentence after the display equation that explains what the formula does in the argument.",
        ),
    )


def _display_text(doc, block) -> str:
    """Display text."""
    lines = doc.source_lines[block.span.start_line - 1 : block.span.end_line]
    inner = [
        line.text.strip()
        for line in lines
        if line.text.strip() and line.text.strip() != "$$"
    ]
    return " ".join(inner)


def _is_nontrivial_display(text: str, min_chars: int) -> bool:
    """Is nontrivial display."""
    compact = text.strip()
    if len(compact) < min_chars:
        return False
    return DISPLAY_OPERATOR_RE.search(compact) is not None


def _next_followup_sentence(blocks, display_index: int):
    """Next followup sentence."""
    for index in range(display_index + 1, len(blocks)):
        block = blocks[index]
        if block.kind in {
            BlockKind.PARAGRAPH,
            BlockKind.BLOCK_QUOTE,
            BlockKind.LIST_ITEM,
        }:
            return block.sentences[0] if block.sentences else None
        if block.kind in {
            BlockKind.HEADING,
            BlockKind.DISPLAY_MATH,
            BlockKind.CODE_BLOCK,
        }:
            return None
    return None


def _is_interpretive_followup(
    sentence,
    interpretation_markers: tuple[str, ...],
    weak_transition_markers: frozenset[str],
    interpretive_noun_pattern,
) -> bool:
    """Is interpretive followup."""
    lowered = sentence.projection.text.lower().strip()
    if not lowered or CONTENT_FREE_FOLLOWUP_RE.fullmatch(lowered):
        return False
    matched = tuple(
        marker.lower()
        for marker in matched_sentence_markers(sentence, interpretation_markers)
    )
    if not matched:
        return False
    if all(marker in weak_transition_markers for marker in matched):
        if sentence_word_count(sentence) <= 6:
            return False
        if interpretive_noun_pattern.search(lowered) is None:
            return False
    return True


def _is_bare_pronoun_followup(sentence) -> bool:
    """Is bare pronoun followup."""
    lowered = sentence.projection.text.lower().strip()
    return bool(
        lowered
        and (
            IT_THEY_OPENING_RE.match(lowered)
            or DEMONSTRATIVE_PREDICATE_RE.match(lowered)
        )
    )


def register(registry) -> None:
    """Register."""
    registry.add(DisplayFollowupInterpretationRule)
