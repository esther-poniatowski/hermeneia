"""Assumption-before-motivation ordering checks."""

from __future__ import annotations

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
from hermeneia.rules.common import iter_sentences, text_has_marker
from hermeneia.rules.patterns import compile_inline_phrase_regex


class AssumptionMotivationOrderRule(HeuristicSemanticRule):
    metadata = RuleMetadata(
        rule_id="math.assumption_motivation_order",
        label="Assumptions should be introduced by purpose",
        layer=Layer.AUDIENCE_FIT,
        tractability=Tractability.CLASS_H,
        kind=RuleKind.RHETORICAL_EXPECTATION,
        default_severity=Severity.INFO,
        supported_languages=frozenset({"en"}),
        default_options={"lookback_sentences": 1},
        evidence_fields=("assumption_marker", "has_prefix_purpose", "previous_has_purpose"),
    )

    def check(self, doc, ctx):
        lookback = self.settings.int_option("lookback_sentences", 1)
        assumption_pattern = compile_inline_phrase_regex(
            tuple(ctx.language_pack.lexicons.assumption_markers)
        )
        purpose_markers = tuple(ctx.language_pack.lexicons.assumption_purpose_markers)
        ordered_sentences = list(iter_sentences(doc))
        violations: list[Violation] = []
        for index, sentence in enumerate(ordered_sentences):
            match = assumption_pattern.search(sentence.projection.text)
            if match is None:
                continue
            prefix = sentence.projection.text[: match.start()].strip()
            has_prefix_purpose = text_has_marker(prefix, purpose_markers)
            if has_prefix_purpose:
                continue
            previous_has_purpose = any(
                text_has_marker(ordered_sentences[prev].source_text, purpose_markers)
                for prev in range(max(0, index - lookback), index)
            )
            if previous_has_purpose:
                continue
            marker = match.group(0).lower()
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    message=(
                        f"Assumption marker '{marker}' appears without a nearby purpose "
                        "statement that explains what it controls."
                    ),
                    span=sentence.span,
                    severity=self.settings.severity,
                    layer=self.metadata.layer,
                    evidence=RuleEvidence(
                        features={
                            "assumption_marker": marker,
                            "has_prefix_purpose": has_prefix_purpose,
                            "previous_has_purpose": previous_has_purpose,
                        }
                    ),
                    confidence=0.74,
                    rationale=(
                        "Assumption-order checks use bounded lexical purpose markers and can "
                        "miss implicit motivation in broader sentence."
                    ),
                    rewrite_tactics=(
                        "State the goal first (for example, stability or uniqueness), then introduce the assumption.",
                    ),
                )
            )
        return violations


def register(registry) -> None:
    registry.add(AssumptionMotivationOrderRule)
