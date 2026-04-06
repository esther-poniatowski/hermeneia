"""Strong-claim calibration against nearby support signals."""

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
from hermeneia.rules.common import iter_sentences


class ClaimCalibrationRule(HeuristicSemanticRule):
    metadata = RuleMetadata(
        rule_id="audience.claim_calibration",
        label="Strong claim lacks nearby evidence cues",
        layer=Layer.AUDIENCE_FIT,
        tractability=Tractability.CLASS_H,
        kind=RuleKind.DIAGNOSTIC_METRIC,
        default_severity=Severity.INFO,
        supported_languages=frozenset({"en"}),
        default_options={"lookback_sentences": 3},
    )

    def check(self, doc, ctx):
        lookback = self.settings.int_option("lookback_sentences", 3)
        markers = tuple(
            marker.lower() for marker in ctx.language_pack.lexicons.strong_claim_markers
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
            lowered = sentence.projection.text.lower()
            matched_markers = tuple(marker for marker in markers if marker in lowered)
            if not matched_markers:
                continue
            signals = ctx.features.support_signals_in_window(
                sentence.id, max_sentences_back=lookback
            )
            strong_support = [signal for signal in signals if signal.kind in evidence_kinds]
            if strong_support:
                continue
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    message="The sentence makes a strong claim without nearby evidence cues.",
                    span=sentence.span,
                    severity=self.settings.severity,
                    layer=self.metadata.layer,
                    evidence=RuleEvidence(
                        features={
                            "claim_markers": matched_markers,
                            "support_signals": tuple(signal.kind.value for signal in signals),
                        },
                        score=0.0,
                        threshold=1.0,
                    ),
                    confidence=0.7,
                    rationale="Claim calibration uses bounded evidence lookback rather than full discourse judgment.",
                    rewrite_tactics=(
                        "Add the supporting citation, result reference, displayed equation, or quantitative evidence near the claim.",
                    ),
                )
            )
        return violations


def register(registry) -> None:
    registry.add(ClaimCalibrationRule)
