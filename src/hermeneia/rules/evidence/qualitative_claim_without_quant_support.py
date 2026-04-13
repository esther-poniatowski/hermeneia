"""Qualitative-claim support checks."""

from __future__ import annotations

import re

from hermeneia.document.indexes import SupportSignalKind
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
from hermeneia.rules.common import iter_sentences, matched_sentence_markers

INLINE_QUANT_RE = re.compile(r"\d|\$")


class QualitativeClaimWithoutQuantSupportRule(HeuristicSemanticRule):
    """Qualitativeclaimwithoutquantsupportrule."""

    metadata = RuleMetadata(
        rule_id="evidence.qualitative_claim_without_quant_support",
        label="Qualitative claim lacks nearby quantitative support",
        layer=Layer.AUDIENCE_FIT,
        tractability=Tractability.CLASS_H,
        kind=RuleKind.DIAGNOSTIC_METRIC,
        default_severity=Severity.INFO,
        supported_languages=frozenset({"en"}),
        default_options={"lookback_sentences": 2},
        abstain_when_flags=frozenset(
            {"heavy_math_masking", "symbol_dense_sentence", "fragment_sentence"}
        ),
        evidence_fields=("claim_markers", "support_signals"),
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
        lookback = self.settings.int_option("lookback_sentences", 2)
        markers = tuple(
            marker.lower()
            for marker in ctx.language_pack.lexicons.qualitative_claim_markers
        )
        evidence_kinds = {
            SupportSignalKind.CITATION,
            SupportSignalKind.THEOREM_REF,
            SupportSignalKind.PROOF_REF,
            SupportSignalKind.DISPLAYED_EQUATION,
            SupportSignalKind.QUANTITATIVE_RESULT,
        }
        violations: list[Violation] = []
        for sentence in iter_sentences(doc):
            if self.should_abstain(sentence.annotation_flags):
                continue
            matched_markers = matched_sentence_markers(sentence, markers)
            if not matched_markers:
                continue
            if INLINE_QUANT_RE.search(sentence.source_text):
                continue
            signals = ctx.features.support_signals_in_window(
                sentence.id, max_sentences_back=lookback
            )
            strong_support = [
                signal for signal in signals if signal.kind in evidence_kinds
            ]
            if strong_support:
                continue
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    message=(
                        "Qualitative performance or stability claim appears without nearby "
                        "quantitative support cues."
                    ),
                    span=sentence.span,
                    severity=self.settings.severity,
                    layer=self.metadata.layer,
                    evidence=RuleEvidence(
                        features={
                            "claim_markers": matched_markers,
                            "support_signals": tuple(
                                signal.kind.value for signal in signals
                            ),
                        },
                        score=0.0,
                        threshold=1.0,
                    ),
                    confidence=0.68,
                    rationale=(
                        "Qualitative-claim calibration uses bounded support signals and cannot "
                        "infer all implicit quantitative backing."
                    ),
                    rewrite_tactics=(
                        "Add a bound, estimate, equation, theorem reference, or citation near the qualitative claim.",
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
    registry.add(QualitativeClaimWithoutQuantSupportRule)
