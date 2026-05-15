"""Passive-voice diagnostics for sentence openings."""

from __future__ import annotations

import re

from hermeneia.document.model import Sentence
from hermeneia.rules.base import (
    AnnotatedRule,
    Layer,
    RuleContext,
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
    """Passivevoicerule."""

    metadata = RuleMetadata(
        rule_id="syntax.passive_voice",
        label="Prefer active voice in sentence openings",
        layer=Layer.SURFACE_STYLE,
        tractability=Tractability.CLASS_B,
        kind=RuleKind.SOFT_HEURISTIC,
        default_severity=Severity.WARNING,
        supported_languages=frozenset({"en"}),
        default_options={
            "apply_block_kinds": ("paragraph",),
            "allow_topic_preserving_passive": True,
            "min_topic_overlap_for_passive_exemption": 0.22,
            "topic_subject_determiners": ("this", "that", "these", "those"),
        },
        abstain_when_flags=frozenset(
            {
                "heavy_math_masking",
                "symbol_dense_sentence",
                "list_item_context",
                "blockquote_context",
                "table_cell_context",
                "heading_context",
            }
        ),
        evidence_fields=("auxiliary", "participle", "dependency_signal"),
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
        allow_topic_preserving = self.settings.bool_option("allow_topic_preserving_passive", True)
        min_topic_overlap = self.settings.float_option(
            "min_topic_overlap_for_passive_exemption", 0.22
        )
        configured_determiners = self.settings.options.get("topic_subject_determiners")
        topic_determiners: tuple[str, ...]
        if isinstance(configured_determiners, str):
            topic_determiners = (configured_determiners,)
        elif isinstance(configured_determiners, (list, tuple)):
            topic_determiners = tuple(
                value
                for value in configured_determiners
                if isinstance(value, str) and value.strip()
            )
        else:
            topic_determiners = ("this", "that", "these", "those")
        sentences = list(iter_sentences(doc))
        violations: list[Violation] = []
        for index, sentence in enumerate(sentences):
            if self.should_abstain(sentence.annotation_flags):
                continue
            passive_signal = _detect_passive_signal(sentence)
            if passive_signal is None:
                continue
            previous = sentences[index - 1] if index > 0 else None
            if (
                allow_topic_preserving
                and previous is not None
                and _is_topic_preserving_passive(
                    previous,
                    sentence,
                    ctx,
                    min_topic_overlap=min_topic_overlap,
                    topic_determiners=topic_determiners,
                )
            ):
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


def _is_topic_preserving_passive(
    previous_sentence: Sentence,
    sentence: Sentence,
    ctx: RuleContext,
    *,
    min_topic_overlap: float,
    topic_determiners: tuple[str, ...],
) -> bool:
    """Topic-preserving passive."""
    if not topic_determiners:
        return False
    determiner_body = "|".join(re.escape(value) for value in topic_determiners)
    subject_pattern = re.compile(
        rf"^\s*(?:{determiner_body})\s+\w+\s+(?:is|are|was|were|be|been|being)\b",
        re.IGNORECASE,
    )
    if subject_pattern.search(sentence.projection.text) is None:
        return False
    overlap = ctx.features.sentence_overlap(previous_sentence.id, sentence.id)
    return overlap >= min_topic_overlap


def _detect_passive_signal(sentence) -> dict[str, object] | None:
    """Detect passive signal."""
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
    """Actor feature."""
    actor = _extract_actor_phrase(sentence)
    if actor is None:
        return {}
    return {"actor": actor}


def _extract_actor_phrase(sentence) -> str | None:
    """Extract actor phrase."""
    match = BY_PHRASE_RE.search(sentence.projection.text)
    if match is None:
        return None
    actor = re.sub(r"\s+", " ", match.group(1)).strip()
    if not actor:
        return None
    return actor


def register(registry) -> None:
    """Register.

    Parameters
    ----------
    registry : object
        Rule registry used to resolve implementations.
    """
    registry.add(PassiveVoiceRule)
