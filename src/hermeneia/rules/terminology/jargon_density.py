"""Audience-specific jargon-density heuristics."""

from __future__ import annotations

import re

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
from hermeneia.rules.common import iter_sentences, upstream_limits

WORD_RE = re.compile(r"\b[A-Za-z][A-Za-z0-9-]*\b")
AUDIENCE_THRESHOLDS = {
    "learner": 0.12,
    "interdisciplinary": 0.16,
    "specialist": 0.24,
}


class JargonDensityRule(HeuristicSemanticRule):
    """Jargondensityrule."""

    metadata = RuleMetadata(
        rule_id="terminology.jargon_density",
        label="Jargon density exceeds audience target",
        layer=Layer.AUDIENCE_FIT,
        tractability=Tractability.CLASS_H,
        kind=RuleKind.SOFT_HEURISTIC,
        default_severity=Severity.INFO,
        supported_languages=frozenset({"en"}),
        evidence_fields=("jargon_terms", "density", "audience"),
    )

    def check(self, doc, ctx):
        """Check."""
        threshold = self.settings.options.get("max_density")
        jargon_terms = ctx.language_pack.lexicons.jargon_terms
        if isinstance(threshold, (int, float)) and not isinstance(threshold, bool):
            max_density = float(threshold)
        else:
            max_density = AUDIENCE_THRESHOLDS.get(ctx.profile.audience, 0.18)
        violations: list[Violation] = []
        for sentence in iter_sentences(doc):
            words = [
                match.group(0).lower()
                for match in WORD_RE.finditer(sentence.projection.text)
            ]
            if len(words) < 6:
                continue
            jargon = [word for word in words if _is_jargon(word, jargon_terms)]
            density = len(jargon) / len(words)
            if density <= max_density:
                continue
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    message=f"Jargon density ({density:.1%}) exceeds the {ctx.profile.audience} audience target.",
                    span=sentence.span,
                    severity=self.settings.severity,
                    layer=self.metadata.layer,
                    evidence=RuleEvidence(
                        features={
                            "jargon_terms": tuple(sorted(set(jargon))),
                            "density": round(density, 3),
                            "audience": ctx.profile.audience,
                        },
                        threshold=max_density,
                        upstream_limits=upstream_limits(sentence),
                    ),
                    confidence=0.64,
                    rationale="Jargon density uses a bounded lexical proxy and audience-specific thresholds.",
                    rewrite_tactics=(
                        "Introduce technical terms with brief glosses and reduce dense "
                        "clusters of specialized terminology.",
                    ),
                )
            )
        return violations


def _is_jargon(word: str, jargon_terms: frozenset[str]) -> bool:
    """Is jargon."""
    if word in jargon_terms:
        return True
    return len(word) >= 12 and word.endswith(
        ("tion", "sion", "metry", "logical", "dynamics", "ization")
    )


def register(registry) -> None:
    """Register."""
    registry.add(JargonDensityRule)
