"""Subordinate-clause load diagnostics."""

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

SUBORDINATE_MARKER_RE = re.compile(
    r"\b(?:although|because|while|whereas|which|that|if|when|since|unless|where)\b",
    re.IGNORECASE,
)
SUBORDINATE_DEP_PREFIXES = ("advcl", "ccomp", "acl", "relcl", "mark")


class SubordinateClauseRule(AnnotatedRule):
    metadata = RuleMetadata(
        rule_id="discourse.subordinate_clause",
        label="Sentence carries too many subordinate clauses",
        layer=Layer.LOCAL_DISCOURSE,
        tractability=Tractability.CLASS_B,
        kind=RuleKind.SOFT_HEURISTIC,
        default_severity=Severity.WARNING,
        supported_languages=frozenset({"en"}),
        default_options={"max_subordinate_clauses": 2},
        abstain_when_flags=frozenset({"heavy_math_masking", "symbol_dense_sentence"}),
        evidence_fields=("subordinate_count", "signal_source"),
    )

    def check(self, doc, ctx):
        max_subordinates = self.settings.int_option("max_subordinate_clauses", 2)
        violations: list[Violation] = []
        for sentence in iter_sentences(doc):
            if self.should_abstain(sentence.annotation_flags):
                continue
            count, source = _subordinate_count(sentence)
            if count <= max_subordinates:
                continue
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    message=f"Sentence appears to stack {count} subordinate clauses.",
                    span=sentence.span,
                    severity=self.settings.severity,
                    layer=self.metadata.layer,
                    evidence=RuleEvidence(
                        features={
                            "subordinate_count": count,
                            "signal_source": source,
                        },
                        threshold=float(max_subordinates),
                        upstream_limits=upstream_limits(sentence),
                    ),
                    confidence=0.74 if source == "dependency" else 0.62,
                    rewrite_tactics=(
                        "Break subordinate material into a follow-up sentence once the main clause is established.",
                    ),
                )
            )
        return violations


def _subordinate_count(sentence) -> tuple[int, str]:
    if sentence.tokens and any(token.dep for token in sentence.tokens):
        count = sum(
            1
            for token in sentence.tokens
            if any((token.dep or "").startswith(prefix) for prefix in SUBORDINATE_DEP_PREFIXES)
        )
        return count, "dependency"
    return len(SUBORDINATE_MARKER_RE.findall(sentence.projection.text)), "regex"


def register(registry) -> None:
    registry.add(SubordinateClauseRule)

