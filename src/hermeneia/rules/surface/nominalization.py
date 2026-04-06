"""Nominalization plus weak-support-verb detection."""

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
        label="Nominalization with weak verbal support",
        layer=Layer.SURFACE_STYLE,
        tractability=Tractability.CLASS_B,
        kind=RuleKind.SOFT_HEURISTIC,
        default_severity=Severity.WARNING,
        supported_languages=frozenset({"en"}),
    )

    def check(self, doc, ctx):
        suffixes = ctx.language_pack.lexicons.nominalization_suffixes
        weak_verbs = ctx.language_pack.lexicons.weak_support_verbs
        violations: list[Violation] = []
        for sentence in iter_sentences(doc):
            if sentence.annotation_flags & {"heavy_math_masking", "symbol_dense_sentence"}:
                continue
            words = [token.lemma.lower() for token in sentence.tokens] or [
                word.lower() for word in re.findall(r"\b\w+\b", sentence.projection.text)
            ]
            for index, word in enumerate(words):
                if len(word) < 6 or not any(word.endswith(suffix) for suffix in suffixes):
                    continue
                neighbors = words[max(0, index - 2) : min(len(words), index + 3)]
                support = next((neighbor for neighbor in neighbors if neighbor in weak_verbs), None)
                if support is None:
                    continue
                violations.append(
                    Violation(
                        rule_id=self.rule_id,
                        message=f"'{word}' is carried by the weak support verb '{support}'; prefer a direct verb construction.",
                        span=sentence.span,
                        severity=self.settings.severity,
                        layer=self.metadata.layer,
                        evidence=RuleEvidence(
                            features={"nominalization": word, "support_verb": support},
                            upstream_limits=upstream_limits(sentence),
                        ),
                        confidence=0.7,
                        rewrite_tactics=(
                            "Replace the process noun with its verbal form if the sentence remains precise.",
                        ),
                    )
                )
                break
        return violations


def register(registry) -> None:
    registry.add(NominalizationRule)
