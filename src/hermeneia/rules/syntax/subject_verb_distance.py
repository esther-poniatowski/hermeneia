"""Subject-to-main-verb distance diagnostics."""

from __future__ import annotations

from hermeneia.rules.base import (
    AnnotatedRule,
    Layer,
    RuleEvidence,
    RuleKind,
    RuleMetadata,
    Severity,
    Tractability,
    Violation,
)
from hermeneia.rules.common import iter_sentences, upstream_limits


class SubjectVerbDistanceRule(AnnotatedRule):
    metadata = RuleMetadata(
        rule_id="syntax.subject_verb_distance",
        label="Subject and main verb are too far apart",
        layer=Layer.LOCAL_DISCOURSE,
        tractability=Tractability.CLASS_B,
        kind=RuleKind.SOFT_HEURISTIC,
        default_severity=Severity.WARNING,
        supported_languages=frozenset({"en"}),
        default_options={"max_distance": 8},
        abstain_when_flags=frozenset(
            {"heavy_math_masking", "symbol_dense_sentence", "fragment_sentence"}
        ),
        evidence_fields=("distance", "subject_token", "root_token"),
    )

    def check(self, doc, ctx):
        max_distance = self.settings.int_option("max_distance", 8)
        violations: list[Violation] = []
        for sentence in iter_sentences(doc):
            if self.should_abstain(sentence.annotation_flags):
                continue
            if not sentence.tokens or not any(token.dep for token in sentence.tokens):
                continue
            root_index = next(
                (index for index, token in enumerate(sentence.tokens) if token.dep == "ROOT"), None
            )
            subject_index = next(
                (
                    index
                    for index, token in enumerate(sentence.tokens)
                    if (token.dep or "").startswith("nsubj")
                ),
                None,
            )
            if root_index is None or subject_index is None:
                continue
            distance = abs(root_index - subject_index)
            if distance <= max_distance:
                continue
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    message=f"The grammatical subject and main verb are separated by {distance} tokens.",
                    span=sentence.span,
                    severity=self.settings.severity,
                    layer=self.metadata.layer,
                    evidence=RuleEvidence(
                        features={
                            "distance": distance,
                            "subject_token": sentence.tokens[subject_index].text,
                            "root_token": sentence.tokens[root_index].text,
                        },
                        threshold=float(max_distance),
                        upstream_limits=upstream_limits(sentence),
                    ),
                    confidence=0.85,
                    rewrite_tactics=(
                        "Move the main verb earlier or postpone parenthetical material until after the clause core is established.",
                    ),
                )
            )
        return violations


def register(registry) -> None:
    registry.add(SubjectVerbDistanceRule)
