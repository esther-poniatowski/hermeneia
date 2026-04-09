"""Nominalization diagnostics with hard-blocker process-noun signals."""

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

SUBJECT_OBJECT_DEPENDENCIES = frozenset(
    {"nsubj", "nsubjpass", "csubj", "obj", "dobj", "pobj", "attr"}
)
HIGH_NOISE_SUFFIXES = frozenset({"al", "ing"})
ADJECTIVE_POSITION_DEPENDENCIES = frozenset({"amod", "compound"})


class NominalizationRule(AnnotatedRule):
    metadata = RuleMetadata(
        rule_id="surface.nominalization",
        label="Nominalization obscures direct action",
        layer=Layer.SURFACE_STYLE,
        tractability=Tractability.CLASS_B,
        kind=RuleKind.HARD_CONSTRAINT,
        default_severity=Severity.ERROR,
        supported_languages=frozenset({"en"}),
        default_options={
            "allow_adjective_position_exception": True,
            "allow_lexicalized_noun_exception": True,
            "extra_lexicalized_nouns": (),
        },
        abstain_when_flags=frozenset({"heavy_math_masking", "symbol_dense_sentence"}),
        evidence_fields=("nominalization", "support_verb", "signal_type"),
    )

    def check(self, doc, ctx):
        allow_adjective_position_exception = self.settings.bool_option(
            "allow_adjective_position_exception",
            True,
        )
        allow_lexicalized_noun_exception = self.settings.bool_option(
            "allow_lexicalized_noun_exception",
            True,
        )
        suffixes = tuple(
            suffix.lower() for suffix in ctx.language_pack.lexicons.nominalization_suffixes
        )
        allowlist = (
            frozenset(term.lower() for term in ctx.language_pack.lexicons.nominalization_allowlist)
            if allow_lexicalized_noun_exception
            else frozenset()
        )
        allowlist = allowlist | _extra_lexicalized_terms(
            self.settings.options.get("extra_lexicalized_nouns")
        )
        weak_verbs = ctx.language_pack.lexicons.weak_support_verbs
        linking_prepositions = ctx.language_pack.lexicons.nominalization_linking_prepositions
        violations: list[Violation] = []
        for sentence in iter_sentences(doc):
            if self.should_abstain(sentence.annotation_flags):
                continue
            nominalization, signal_type, support_verb = _detect_nominalization(
                sentence,
                suffixes=suffixes,
                allowlist=allowlist,
                weak_verbs=weak_verbs,
                linking_prepositions=linking_prepositions,
                allow_adjective_position_exception=allow_adjective_position_exception,
            )
            if nominalization is None or signal_type is None:
                continue
            message = (
                f"'{nominalization}' is carried by the weak support verb '{support_verb}'; "
                "prefer a direct verb construction."
                if signal_type == "weak_support_verb"
                else (
                    f"'{nominalization}' appears in an abstract noun phrase; "
                    "prefer a direct verb construction."
                    if signal_type == "abstract_noun_phrase"
                    else (
                        f"'{nominalization}' is a process noun in a core argument position; "
                        "prefer an explicit verb form."
                        if signal_type == "core_argument_nominalization"
                        else (
                            f"'{nominalization}' functions as a process noun; "
                            "prefer an explicit verb form."
                        )
                    )
                )
            )
            confidence = (
                0.9
                if signal_type == "weak_support_verb"
                else 0.86
                if signal_type == "abstract_noun_phrase"
                else 0.82
                if signal_type == "core_argument_nominalization"
                else 0.76
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


def _detect_nominalization(
    sentence,
    *,
    suffixes: tuple[str, ...],
    allowlist: frozenset[str],
    weak_verbs: frozenset[str],
    linking_prepositions: frozenset[str],
    allow_adjective_position_exception: bool,
) -> tuple[str | None, str | None, str | None]:
    if sentence.tokens:
        return _detect_from_tokens(
            sentence.tokens,
            suffixes=suffixes,
            allowlist=allowlist,
            weak_verbs=weak_verbs,
            linking_prepositions=linking_prepositions,
            allow_adjective_position_exception=allow_adjective_position_exception,
        )
    return _detect_from_text(
        sentence.projection.text,
        suffixes=suffixes,
        allowlist=allowlist,
        weak_verbs=weak_verbs,
        linking_prepositions=linking_prepositions,
    )


def _detect_from_tokens(
    tokens,
    *,
    suffixes: tuple[str, ...],
    allowlist: frozenset[str],
    weak_verbs: frozenset[str],
    linking_prepositions: frozenset[str],
    allow_adjective_position_exception: bool,
) -> tuple[str | None, str | None, str | None]:
    words = [_lemma(token) for token in tokens]
    candidate_indexes = [
        index
        for index, word in enumerate(words)
        if _token_is_candidate(
            token=tokens[index],
            lemma=word,
            next_word=words[index + 1] if index + 1 < len(words) else None,
            next_token=tokens[index + 1] if index + 1 < len(tokens) else None,
            suffixes=suffixes,
            allowlist=allowlist,
            linking_prepositions=linking_prepositions,
            allow_adjective_position_exception=allow_adjective_position_exception,
        )
    ]
    if not candidate_indexes:
        return None, None, None

    for index in candidate_indexes:
        neighbors = words[max(0, index - 2) : min(len(words), index + 3)]
        support = next((neighbor for neighbor in neighbors if neighbor in weak_verbs), None)
        if support is not None:
            return words[index], "weak_support_verb", support

    for index in candidate_indexes:
        next_word = words[index + 1] if index + 1 < len(words) else None
        if next_word in linking_prepositions:
            return words[index], "abstract_noun_phrase", None

    for index in candidate_indexes:
        dependency = (tokens[index].dep or "").lower()
        if dependency in SUBJECT_OBJECT_DEPENDENCIES:
            return words[index], "core_argument_nominalization", None

    if not allow_adjective_position_exception:
        for index in candidate_indexes:
            next_token = tokens[index + 1] if index + 1 < len(tokens) else None
            if _is_adjective_position(tokens[index], next_token):
                return words[index], "adjective_position_nominalization", None

    if len(candidate_indexes) >= 2:
        return words[candidate_indexes[0]], "stacked_nominalizations", None

    return None, None, None


def _detect_from_text(
    text: str,
    *,
    suffixes: tuple[str, ...],
    allowlist: frozenset[str],
    weak_verbs: frozenset[str],
    linking_prepositions: frozenset[str],
) -> tuple[str | None, str | None, str | None]:
    words = [word.lower() for word in re.findall(r"\b\w+\b", text)]
    candidate_indexes: list[int] = []
    for index, word in enumerate(words):
        next_word = words[index + 1] if index + 1 < len(words) else None
        if _text_word_is_candidate(
            word=word,
            next_word=next_word,
            suffixes=suffixes,
            allowlist=allowlist,
            linking_prepositions=linking_prepositions,
        ):
            candidate_indexes.append(index)
    if not candidate_indexes:
        return None, None, None

    for index in candidate_indexes:
        neighbors = words[max(0, index - 2) : min(len(words), index + 3)]
        support = next((neighbor for neighbor in neighbors if neighbor in weak_verbs), None)
        if support is not None:
            return words[index], "weak_support_verb", support

    for index in candidate_indexes:
        next_word = words[index + 1] if index + 1 < len(words) else None
        if next_word in linking_prepositions:
            return words[index], "abstract_noun_phrase", None

    if len(candidate_indexes) >= 2:
        return words[candidate_indexes[0]], "stacked_nominalizations", None

    return None, None, None


def _token_is_candidate(
    *,
    token,
    lemma: str,
    next_word: str | None,
    next_token,
    suffixes: tuple[str, ...],
    allowlist: frozenset[str],
    linking_prepositions: frozenset[str],
    allow_adjective_position_exception: bool,
) -> bool:
    if not _is_suffix_candidate(lemma, suffixes, allowlist):
        return False
    if allow_adjective_position_exception and _is_adjective_position(token, next_token):
        return False
    suffix = _matching_suffix(lemma, suffixes)
    if suffix in HIGH_NOISE_SUFFIXES:
        pos = (token.pos or "").upper()
        dependency = (token.dep or "").lower()
        if pos not in {"NOUN", "PROPN"} and dependency not in SUBJECT_OBJECT_DEPENDENCIES:
            return False
        if next_word not in linking_prepositions and dependency not in SUBJECT_OBJECT_DEPENDENCIES:
            return False
    return True


def _text_word_is_candidate(
    *,
    word: str,
    next_word: str | None,
    suffixes: tuple[str, ...],
    allowlist: frozenset[str],
    linking_prepositions: frozenset[str],
) -> bool:
    if not _is_suffix_candidate(word, suffixes, allowlist):
        return False
    suffix = _matching_suffix(word, suffixes)
    if suffix in HIGH_NOISE_SUFFIXES and next_word not in linking_prepositions:
        return False
    return True


def _extra_lexicalized_terms(raw: object) -> frozenset[str]:
    if raw is None:
        return frozenset()
    if isinstance(raw, str):
        value = raw.strip().lower()
        return frozenset({value}) if value else frozenset()
    if not isinstance(raw, (list, tuple, set, frozenset)):
        return frozenset()
    values: set[str] = set()
    for item in raw:
        value = str(item).strip().lower()
        if value:
            values.add(value)
    return frozenset(values)


def _is_adjective_position(token, next_token) -> bool:
    dependency = (token.dep or "").lower()
    if dependency in ADJECTIVE_POSITION_DEPENDENCIES:
        return True
    if next_token is None:
        return False
    token_pos = (token.pos or "").upper()
    next_pos = (next_token.pos or "").upper()
    return token_pos in {"NOUN", "PROPN"} and next_pos in {"NOUN", "PROPN"} and dependency == "compound"


def _is_suffix_candidate(word: str, suffixes: tuple[str, ...], allowlist: frozenset[str]) -> bool:
    if len(word) < 6:
        return False
    if word in allowlist:
        return False
    return any(word.endswith(suffix) for suffix in suffixes)


def _matching_suffix(word: str, suffixes: tuple[str, ...]) -> str | None:
    for suffix in suffixes:
        if word.endswith(suffix):
            return suffix
    return None


def _lemma(token) -> str:
    return (token.lemma or token.text).lower()
