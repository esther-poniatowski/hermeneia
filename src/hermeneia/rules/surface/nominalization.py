"""Nominalization diagnostics with explicit abstraction signals."""

from __future__ import annotations

import re

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


class NominalizationRule(AnnotatedRule):
    metadata = RuleMetadata(
        rule_id="surface.nominalization",
        label="Nominalization obscures direct action",
        layer=Layer.SURFACE_STYLE,
        tractability=Tractability.CLASS_B,
        kind=RuleKind.SOFT_HEURISTIC,
        default_severity=Severity.WARNING,
        supported_languages=frozenset({"en"}),
        abstain_when_flags=frozenset({"heavy_math_masking", "symbol_dense_sentence"}),
        evidence_fields=("nominalization", "support_verb", "signal_type"),
    )

    def check(self, doc, ctx):
        suffixes = ctx.language_pack.lexicons.nominalization_suffixes
        weak_verbs = ctx.language_pack.lexicons.weak_support_verbs
        linking_prepositions = ctx.language_pack.lexicons.nominalization_linking_prepositions
        violations: list[Violation] = []
        for sentence in iter_sentences(doc):
            if self.should_abstain(sentence.annotation_flags):
                continue
            words = [token.lemma.lower() for token in sentence.tokens] or [
                word.lower() for word in re.findall(r"\b\w+\b", sentence.projection.text)
            ]
            candidate_indexes = [
                index
                for index, word in enumerate(words)
                if len(word) >= 6 and any(word.endswith(suffix) for suffix in suffixes)
            ]
            if not candidate_indexes:
                continue

            selected_index: int | None = None
            support_verb: str | None = None
            signal_type: str | None = None

            for index in candidate_indexes:
                neighbors = words[max(0, index - 2) : min(len(words), index + 3)]
                support = next(
                    (neighbor for neighbor in neighbors if neighbor in weak_verbs), None
                )
                if support is None:
                    continue
                selected_index = index
                support_verb = support
                signal_type = "weak_support_verb"
                break

            if selected_index is None:
                for index in candidate_indexes:
                    if index + 1 >= len(words):
                        continue
                    if words[index + 1] in linking_prepositions:
                        selected_index = index
                        signal_type = "abstract_noun_phrase"
                        break

            if selected_index is None and len(candidate_indexes) >= 2:
                selected_index = candidate_indexes[0]
                signal_type = "stacked_nominalizations"

            if selected_index is None or signal_type is None:
                continue
            nominalization = words[selected_index]
            message = (
                f"'{nominalization}' is carried by the weak support verb '{support_verb}'; "
                "prefer a direct verb construction."
                if signal_type == "weak_support_verb"
                else f"'{nominalization}' appears in an abstract noun phrase; prefer a direct verb construction."
            )
            confidence = (
                0.78
                if signal_type == "weak_support_verb"
                else 0.72
                if signal_type == "abstract_noun_phrase"
                else 0.64
            )
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    message=message,
                    span=sentence.span,
                    severity=self.settings.severity,
                    layer=self.metadata.layer,
                    evidence=RuleEvidence(
                        features={
                            "nominalization": nominalization,
                            "support_verb": support_verb,
                            "signal_type": signal_type,
                        },
                        upstream_limits=upstream_limits(sentence),
                    ),
                    confidence=confidence,
                    rewrite_tactics=(
                        "Replace the process noun with a direct verb phrase when precision is preserved.",
                    ),
                )
            )
        return violations


def register(registry) -> None:
    registry.add(NominalizationRule)
