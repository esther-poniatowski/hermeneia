"""Noun-cluster density checks."""

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

WORD_RE = re.compile(r"\b[A-Za-z][A-Za-z0-9-]*\b")
NOUNISH_POS = frozenset({"NOUN", "PROPN", "ADJ"})


class NounClusterRule(AnnotatedRule):
    """Nounclusterrule."""

    metadata = RuleMetadata(
        rule_id="vocabulary.noun_cluster",
        label="Sentence contains an overloaded noun cluster",
        layer=Layer.SURFACE_STYLE,
        tractability=Tractability.CLASS_B,
        kind=RuleKind.SOFT_HEURISTIC,
        default_severity=Severity.WARNING,
        supported_languages=frozenset({"en"}),
        default_options={"max_cluster_tokens": 4},
        abstain_when_flags=frozenset({"heavy_math_masking", "symbol_dense_sentence"}),
        evidence_fields=("cluster_length", "cluster"),
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
        max_cluster = self.settings.int_option("max_cluster_tokens", 4)
        violations: list[Violation] = []
        for sentence in iter_sentences(doc):
            if self.should_abstain(sentence.annotation_flags):
                continue
            cluster = _max_cluster(sentence)
            if len(cluster) <= max_cluster:
                continue
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    message=f"Detected a {len(cluster)}-token noun cluster; unpack the modifiers.",
                    span=sentence.span,
                    severity=self.settings.severity,
                    layer=self.metadata.layer,
                    evidence=RuleEvidence(
                        features={
                            "cluster_length": len(cluster),
                            "cluster": tuple(cluster),
                        },
                        threshold=float(max_cluster),
                        upstream_limits=upstream_limits(sentence),
                    ),
                    confidence=0.68,
                    rewrite_tactics=(
                        "Convert part of the noun stack into a clause or use "
                        "prepositions to make relationships explicit.",
                    ),
                )
            )
        return violations


def _max_cluster(sentence) -> list[str]:
    """Max cluster."""
    if sentence.tokens and any(token.pos is not None for token in sentence.tokens):
        longest: list[str] = []
        current: list[str] = []
        for token in sentence.tokens:
            if token.pos in NOUNISH_POS:
                current.append(token.text)
                if len(current) > len(longest):
                    longest = current[:]
            else:
                current = []
        return longest
    words = [match.group(0) for match in WORD_RE.finditer(sentence.projection.text)]
    if len(words) >= 5:
        return words[:5]
    return words


def register(registry) -> None:
    """Register.

    Parameters
    ----------
    registry : object
        Rule registry used to resolve implementations.
    """
    registry.add(NounClusterRule)
