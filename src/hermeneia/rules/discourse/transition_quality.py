"""Connector-driven transition support-gap heuristics."""

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
from hermeneia.rules.common import iter_sentences

LEADING_CONNECTOR_RE = re.compile(
    r"^\s*(however|therefore|thus|hence|consequently|accordingly|in contrast|conversely)\b",
    re.IGNORECASE,
)


class TransitionQualityRule(HeuristicSemanticRule):
    metadata = RuleMetadata(
        rule_id="discourse.transition_quality",
        label="Transition marker lacks nearby support cues",
        layer=Layer.LOCAL_DISCOURSE,
        tractability=Tractability.CLASS_H,
        kind=RuleKind.DIAGNOSTIC_METRIC,
        default_severity=Severity.INFO,
        supported_languages=frozenset({"en"}),
        default_options={"lookback_sentences": 2},
        evidence_fields=("connector", "support_signals"),
    )

    def check(self, doc, ctx):
        lookback = self.settings.int_option("lookback_sentences", 2)
        evidence_kinds = {
            SupportSignalKind.CITATION,
            SupportSignalKind.THEOREM_REF,
            SupportSignalKind.PROOF_REF,
            SupportSignalKind.DISPLAYED_EQUATION,
            SupportSignalKind.QUANTITATIVE_RESULT,
        }
        violations: list[Violation] = []
        for sentence in iter_sentences(doc):
            match = LEADING_CONNECTOR_RE.search(sentence.projection.text)
            if match is None:
                continue
            connector = match.group(1).lower()
            signals = ctx.features.support_signals_in_window(
                sentence.id, max_sentences_back=lookback
            )
            strong_signals = [signal for signal in signals if signal.kind in evidence_kinds]
            if strong_signals:
                continue
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    message=f"Transition marker '{connector}' is not anchored by nearby support cues.",
                    span=sentence.span,
                    severity=self.settings.severity,
                    layer=self.metadata.layer,
                    evidence=RuleEvidence(
                        features={
                            "connector": connector,
                            "support_signals": tuple(signal.kind.value for signal in signals),
                        },
                        score=0.0,
                        threshold=1.0,
                    ),
                    confidence=0.64,
                    rationale="Transition quality uses bounded support lookback rather than full discourse parsing.",
                    rewrite_tactics=(
                        "Add the concrete support, evidence, or contrast basis that motivates the transition marker.",
                    ),
                )
            )
        return violations


def register(registry) -> None:
    registry.add(TransitionQualityRule)
