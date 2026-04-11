"""Passive-voice diagnostics for sentence openings."""

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

PASSIVE_FALLBACK_RE = re.compile(
    r"\b(?:is|are|was|were|be|been|being)\s+\w+(?:ed|en)\b", re.IGNORECASE
)
BY_PHRASE_RE = re.compile(r"\bby\s+([A-Za-z][A-Za-z0-9' -]{0,80}?)(?=[,.;:!?]|$)", re.IGNORECASE)


class PassiveVoiceRule(AnnotatedRule):
    metadata = RuleMetadata(
        rule_id="syntax.passive_voice",
        label="Prefer active voice in sentence openings",
        layer=Layer.SURFACE_STYLE,
        tractability=Tractability.CLASS_B,
        kind=RuleKind.SOFT_HEURISTIC,
        default_severity=Severity.WARNING,
        supported_languages=frozenset({"en"}),
        abstain_when_flags=frozenset({"heavy_math_masking", "symbol_dense_sentence"}),
        evidence_fields=("auxiliary", "participle", "dependency_signal"),
    )

    def check(self, doc, ctx):
        violations: list[Violation] = []
        for sentence in iter_sentences(doc):
            if self.should_abstain(sentence.annotation_flags):
                continue
            passive_signal = _detect_passive_signal(sentence)
            if passive_signal is None:
                continue
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    message="The sentence appears to use passive voice; prefer an explicit actor when possible.",
                    span=sentence.span,
                    severity=self.settings.severity,
                    layer=self.metadata.layer,
                    evidence=RuleEvidence(
                        features=passive_signal,
                        upstream_limits=upstream_limits(sentence),
                    ),
                    confidence=0.72,
                    rewrite_tactics=(
                        "Rewrite the clause so the actor appears as the grammatical subject where precision allows.",
                    ),
                )
            )
        return violations


def _detect_passive_signal(sentence) -> dict[str, object] | None:
    tokens = sentence.tokens
    if tokens and any((token.dep or "").endswith("pass") for token in tokens):
        aux = next(
            (token.text for token in tokens if (token.dep or "") in {"auxpass", "aux"}),
            None,
        )
        participle = next(
            (
                token.text
                for token in tokens
                if token.pos == "VERB" and token.text.lower().endswith(("ed", "en"))
            ),
            None,
        )
        return {
            "auxiliary": aux,
            "participle": participle,
            "dependency_signal": "passive_dependency",
            **_actor_feature(sentence),
        }
    match = PASSIVE_FALLBACK_RE.search(sentence.projection.text)
    if match is None:
        return None
    phrase = match.group(0).split()
    auxiliary = phrase[0] if phrase else None
    participle = phrase[1] if len(phrase) > 1 else None
    return {
        "auxiliary": auxiliary,
        "participle": participle,
        "dependency_signal": "regex_fallback",
        **_actor_feature(sentence),
    }


def _actor_feature(sentence) -> dict[str, str]:
    actor = _extract_actor_phrase(sentence)
    if actor is None:
        return {}
    return {"actor": actor}


def _extract_actor_phrase(sentence) -> str | None:
    match = BY_PHRASE_RE.search(sentence.projection.text)
    if match is None:
        return None
    actor = re.sub(r"\s+", " ", match.group(1)).strip()
    if not actor:
        return None
    return actor


def register(registry) -> None:
    registry.add(PassiveVoiceRule)
