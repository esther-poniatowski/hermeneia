"""Detect imprecise quantity references without citation support."""

from __future__ import annotations

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


class ImpreciseQuantifierWithoutCitationRule(HeuristicSemanticRule):
    """Imprecisequantifierwithoutcitationrule."""

    metadata = RuleMetadata(
        rule_id="evidence.imprecise_quantifier_without_citation",
        label="Imprecise quantifier references should carry citation support",
        layer=Layer.AUDIENCE_FIT,
        tractability=Tractability.CLASS_H,
        kind=RuleKind.DIAGNOSTIC_METRIC,
        default_severity=Severity.INFO,
        supported_languages=frozenset({"en"}),
        default_options={"lookback_sentences": 0},
        abstain_when_flags=frozenset(
            {"heavy_math_masking", "symbol_dense_sentence", "fragment_sentence"}
        ),
        evidence_fields=("quantifiers", "support_signals"),
    )

    def check(self, doc, ctx):
        """Check."""
        lookback = self.settings.int_option("lookback_sentences", 0)
        quantifiers = tuple(ctx.language_pack.lexicons.imprecise_quantifier_terms)
        violations: list[Violation] = []
        for sentence in iter_sentences(doc):
            if self.should_abstain(sentence.annotation_flags):
                continue
            matched_quantifiers = matched_sentence_markers(sentence, quantifiers)
            if not matched_quantifiers:
                continue
            signals = ctx.features.support_signals_in_window(
                sentence.id,
                max_sentences_back=max(0, lookback),
            )
            citations = [
                signal
                for signal in signals
                if signal.kind == SupportSignalKind.CITATION
            ]
            if citations:
                continue
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    message=(
                        "Imprecise quantifier phrasing (for example, 'several' or 'others') "
                        "should be backed by a nearby citation."
                    ),
                    span=sentence.span,
                    severity=self.settings.severity,
                    layer=self.metadata.layer,
                    evidence=RuleEvidence(
                        features={
                            "quantifiers": matched_quantifiers,
                            "support_signals": tuple(
                                signal.kind.value for signal in signals
                            ),
                        },
                        score=0.0,
                        threshold=1.0,
                    ),
                    confidence=0.74,
                    rationale=(
                        "The rule triggers only when imprecise quantity markers appear without "
                        "nearby citation support."
                    ),
                    rewrite_tactics=(
                        "Add a citation or replace the vague quantifier with specific, sourced evidence.",
                    ),
                )
            )
        return violations


def register(registry) -> None:
    """Register."""
    registry.add(ImpreciseQuantifierWithoutCitationRule)
