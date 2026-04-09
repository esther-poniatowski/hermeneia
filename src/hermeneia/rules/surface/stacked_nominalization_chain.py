"""Detect stacked nominalization chains in a single phrase."""

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
from hermeneia.rules.common import iter_sentences

WORD_RE = re.compile(r"\b[A-Za-z][A-Za-z0-9-]*\b")
CHAIN_CONNECTORS = frozenset({"of", "and", "the", "for", "to", "in", "with"})
HIGH_NOISE_SUFFIXES = frozenset({"al", "ing"})


class StackedNominalizationChainRule(AnnotatedRule):
    metadata = RuleMetadata(
        rule_id="surface.stacked_nominalization_chain",
        label="Avoid stacked nominalization chains",
        layer=Layer.SURFACE_STYLE,
        tractability=Tractability.CLASS_B,
        kind=RuleKind.HARD_CONSTRAINT,
        default_severity=Severity.ERROR,
        supported_languages=frozenset({"en"}),
        default_options={"min_chain": 3},
        evidence_fields=("chain_length", "nominalizations"),
    )

    def check(self, doc, ctx):
        min_chain = self.settings.int_option("min_chain", 3)
        suffixes = tuple(
            suffix.lower() for suffix in ctx.language_pack.lexicons.nominalization_suffixes
        )
        allowlist = frozenset(
            term.lower() for term in ctx.language_pack.lexicons.nominalization_allowlist
        )
        violations: list[Violation] = []
        for sentence in iter_sentences(doc):
            chain = _largest_chain(
                sentence,
                suffixes=suffixes,
                allowlist=allowlist,
            )
            if len(chain) < min_chain:
                continue
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    message=(
                        f"Detected a {len(chain)}-term nominalization chain; "
                        "rewrite with explicit verbs and simpler phrase structure."
                    ),
                    span=sentence.span,
                    severity=self.settings.severity,
                    layer=self.metadata.layer,
                    evidence=RuleEvidence(
                        features={
                            "chain_length": len(chain),
                            "nominalizations": tuple(chain),
                        },
                        score=float(len(chain)),
                        threshold=float(min_chain),
                    ),
                    confidence=0.83,
                    rewrite_tactics=(
                        "Break the chain into clauses that name actions and their arguments directly.",
                    ),
                )
            )
        return violations


def _largest_chain(
    sentence,
    *,
    suffixes: tuple[str, ...],
    allowlist: frozenset[str],
) -> list[str]:
    if sentence.tokens:
        words = [_token_word(token) for token in sentence.tokens]
        poses = [(token.pos or "").upper() for token in sentence.tokens]
        return _largest_chain_from_words(words, suffixes, allowlist, poses=poses)
    words = [match.group(0).lower() for match in WORD_RE.finditer(sentence.projection.text)]
    return _largest_chain_from_words(words, suffixes, allowlist, poses=None)


def _largest_chain_from_words(
    words: list[str],
    suffixes: tuple[str, ...],
    allowlist: frozenset[str],
    *,
    poses: list[str] | None,
) -> list[str]:
    best: list[str] = []
    current: list[str] = []
    for index, word in enumerate(words):
        pos = poses[index] if poses is not None and index < len(poses) else None
        if _is_nominalization(word, suffixes, allowlist, pos=pos):
            current.append(word)
            if len(current) > len(best):
                best = current[:]
            continue
        if current and word in CHAIN_CONNECTORS:
            continue
        current = []
    return best


def _is_nominalization(
    word: str,
    suffixes: tuple[str, ...],
    allowlist: frozenset[str],
    *,
    pos: str | None,
) -> bool:
    if len(word) < 6 or word in allowlist:
        return False
    suffix = _matching_suffix(word, suffixes)
    if suffix is None:
        return False
    if suffix in HIGH_NOISE_SUFFIXES and pos not in {None, "NOUN", "PROPN"}:
        return False
    return True


def _matching_suffix(word: str, suffixes: tuple[str, ...]) -> str | None:
    for suffix in suffixes:
        if word.endswith(suffix):
            return suffix
    return None


def _token_word(token) -> str:
    return (token.lemma or token.text).lower()


def register(registry) -> None:
    registry.add(StackedNominalizationChainRule)
