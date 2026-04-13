"""Proof-placement context checks."""

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
from hermeneia.rules.common import previous_prose_block, text_has_marker
from hermeneia.rules.patterns import compile_leading_phrase_regex

PROOF_OPENER_RE = re.compile(r"^\s*proof\.?\s*$", re.IGNORECASE)


class ProofPlacementContextRule(HeuristicSemanticRule):
    """Proofplacementcontextrule."""

    metadata = RuleMetadata(
        rule_id="math.proof_placement_context",
        label="Proof opener should follow interpretive context",
        layer=Layer.DOCUMENT_STRUCTURE,
        tractability=Tractability.CLASS_H,
        kind=RuleKind.RHETORICAL_EXPECTATION,
        default_severity=Severity.INFO,
        supported_languages=frozenset({"en"}),
        evidence_fields=("issue", "previous_block_kind"),
    )

    def check(self, doc, ctx):
        """Check.

        Parameters
        ----------
        doc : object
            Document instance to inspect.
        ctx : object
            Rule evaluation context.

        Returns
        -------
        object
            Resulting value produced by this call.
        """
        interpretation_markers = tuple(
            ctx.language_pack.lexicons.formula_interpretation_markers
        )
        formal_statement_pattern = compile_leading_phrase_regex(
            tuple(ctx.language_pack.lexicons.proof_context_formal_openers)
        )
        flat_blocks = list(doc.iter_blocks())
        violations: list[Violation] = []
        for index, block in enumerate(flat_blocks):
            if block.kind != BlockKind.PARAGRAPH or not block.sentences:
                continue
            first_sentence = block.sentences[0].source_text.strip()
            if PROOF_OPENER_RE.fullmatch(first_sentence) is None:
                continue
            previous = previous_prose_block(flat_blocks, index)
            if previous is None or not previous.sentences:
                continue
            previous_text = " ".join(
                sentence.source_text for sentence in previous.sentences
            )
            if formal_statement_pattern.search(previous_text) is None:
                continue
            if text_has_marker(previous_text, interpretation_markers):
                continue
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    message=(
                        "Proof starts immediately after a formal statement without an "
                        "interpretive bridge."
                    ),
                    span=block.span,
                    severity=self.settings.severity,
                    layer=self.metadata.layer,
                    evidence=RuleEvidence(
                        features={
                            "issue": "proof_after_formal_without_interpretation",
                            "previous_block_kind": previous.kind.value,
                            "previous_block_id": previous.id,
                        }
                    ),
                    confidence=0.69,
                    rationale=(
                        "Proof-placement checks only immediate local context and cannot infer "
                        "broader interpretive intent."
                    ),
                    rewrite_tactics=(
                        "Insert one paragraph that explains what the formal statement controls before '*Proof.*'.",
                    ),
                )
            )
        return violations


def register(registry) -> None:
    """Register.

    Parameters
    ----------
    registry : object
        Rule registry used to resolve implementations.
    """
    registry.add(ProofPlacementContextRule)
