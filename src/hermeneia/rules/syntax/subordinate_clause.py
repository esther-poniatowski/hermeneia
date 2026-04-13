"""Subordinate-clause load diagnostics."""

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
from hermeneia.rules.patterns import compile_inline_phrase_regex

SUBORDINATE_DEP_PREFIXES = ("advcl", "ccomp", "acl", "relcl", "mark")


class SubordinateClauseRule(AnnotatedRule):
    """Subordinateclauserule."""

    metadata = RuleMetadata(
        rule_id="syntax.subordinate_clause",
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
        max_subordinates = self.settings.int_option("max_subordinate_clauses", 2)
        marker_pattern = compile_inline_phrase_regex(
            tuple(ctx.language_pack.lexicons.subordinate_clause_markers)
        )
        violations: list[Violation] = []
        for sentence in iter_sentences(doc):
            if self.should_abstain(sentence.annotation_flags):
                continue
            count, source = _subordinate_count(sentence, marker_pattern)
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


def _subordinate_count(sentence, marker_pattern) -> tuple[int, str]:
    """Subordinate count."""
    if sentence.tokens and any(token.dep for token in sentence.tokens):
        count = sum(
            1
            for token in sentence.tokens
            if any(
                (token.dep or "").startswith(prefix)
                for prefix in SUBORDINATE_DEP_PREFIXES
            )
        )
        return count, "dependency"
    return sum(1 for _ in marker_pattern.finditer(sentence.projection.text)), "regex"


def register(registry) -> None:
    """Register.

    Parameters
    ----------
    registry : object
        Rule registry used to resolve implementations.
    """
    registry.add(SubordinateClauseRule)
