"""Prepositional-chain density diagnostics."""

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

WORD_RE = re.compile(r"\b[A-Za-z]+\b")


class PrepChainRule(AnnotatedRule):
    metadata = RuleMetadata(
        rule_id="vocabulary.prep_chain",
        label="Sentence has dense prepositional chaining",
        layer=Layer.SURFACE_STYLE,
        tractability=Tractability.CLASS_A,
        kind=RuleKind.SOFT_HEURISTIC,
        default_severity=Severity.WARNING,
        supported_languages=frozenset({"en"}),
        default_options={"max_prepositions": 4},
        evidence_fields=("preposition_count", "prepositions"),
    )

    def check(self, doc, ctx):
        max_prepositions = self.settings.int_option("max_prepositions", 4)
        preposition_set = ctx.language_pack.lexicons.prepositions
        violations: list[Violation] = []
        for sentence in iter_sentences(doc):
            words = _words(sentence)
            prepositions = [word for word in words if word in preposition_set]
            count = len(prepositions)
            if count <= max_prepositions:
                continue
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    message=f"Sentence contains {count} prepositions, which can obscure the clause core.",
                    span=sentence.span,
                    severity=self.settings.severity,
                    layer=self.metadata.layer,
                    evidence=RuleEvidence(
                        features={
                            "preposition_count": count,
                            "prepositions": tuple(prepositions[:8]),
                        },
                        threshold=float(max_prepositions),
                        upstream_limits=upstream_limits(sentence),
                    ),
                    confidence=0.66,
                    rewrite_tactics=(
                        "Replace prepositional stacking with direct verbs or split the sentence into shorter clauses.",
                    ),
                )
            )
        return violations


def _words(sentence) -> list[str]:
    if sentence.tokens:
        return [token.lemma.lower() for token in sentence.tokens]
    return [match.group(0).lower() for match in WORD_RE.finditer(sentence.projection.text)]


def register(registry) -> None:
    registry.add(PrepChainRule)
