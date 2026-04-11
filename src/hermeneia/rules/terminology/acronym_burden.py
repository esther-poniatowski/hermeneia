"""Acronym-definition and acronym-overuse checks."""

from __future__ import annotations

from dataclasses import dataclass
import re

from hermeneia.document.model import Sentence
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

ACRONYM_RE = re.compile(r"\b[A-Z]{2,}(?:s)?\b")
FULL_FORM_THEN_ACRONYM_RE = re.compile(
    r"\b(?P<full>[A-Za-z][A-Za-z0-9-]*(?:\s+[A-Za-z][A-Za-z0-9-]*){1,7})\s*"
    r"\((?P<acronym>[A-Z]{2,}(?:s)?)\)"
)
ACRONYM_THEN_FULL_FORM_RE = re.compile(
    r"\b(?P<acronym>[A-Z]{2,}(?:s)?)\s*"
    r"\((?P<full>[A-Za-z][A-Za-z0-9-]*(?:\s+[A-Za-z][A-Za-z0-9-]*){1,7})\)"
)
WORD_RE = re.compile(r"[A-Za-z][A-Za-z0-9-]*")


@dataclass(frozen=True)
class AcronymDefinition:
    acronym: str
    full_form: str
    sentence_id: str
    sentence_ordinal: int


class AcronymBurdenRule(AnnotatedRule):
    metadata = RuleMetadata(
        rule_id="terminology.acronym_burden",
        label="Acronyms should be defined first and kept secondary to full forms",
        layer=Layer.AUDIENCE_FIT,
        tractability=Tractability.CLASS_A,
        kind=RuleKind.SOFT_HEURISTIC,
        default_severity=Severity.WARNING,
        supported_languages=frozenset({"en"}),
        default_options={
            "min_acronym_mentions_for_overuse": 4,
            "max_acronym_to_full_form_ratio": 2.0,
        },
        evidence_fields=(
            "issue",
            "acronym",
            "full_form",
            "acronym_mentions",
            "full_form_mentions",
        ),
    )

    def check(self, doc, ctx):
        min_mentions_for_overuse = self.settings.int_option("min_acronym_mentions_for_overuse", 4)
        max_ratio = self.settings.float_option("max_acronym_to_full_form_ratio", 2.0)
        allowlist = ctx.language_pack.lexicons.acronym_allowlist
        definition_stopwords = ctx.language_pack.lexicons.acronym_definition_stopwords
        ordinal_by_sentence_id = {ref.id: ref.ordinal for ref in doc.indexes.sentences}
        definitions = _collect_definitions(
            doc, allowlist, ordinal_by_sentence_id, definition_stopwords
        )
        mentions = _collect_mentions(doc, allowlist, ordinal_by_sentence_id)
        violations: list[Violation] = []

        for acronym, sentence_mentions in sorted(mentions.items()):
            if not sentence_mentions:
                continue
            definition = definitions.get(acronym)
            first_ordinal, first_sentence = sentence_mentions[0]
            if definition is None or first_ordinal < definition.sentence_ordinal:
                violations.append(
                    Violation(
                        rule_id=self.rule_id,
                        message=(
                            f"Acronym '{acronym}' appears before any local full-form definition."
                        ),
                        span=first_sentence.span,
                        severity=self.settings.severity,
                        layer=self.metadata.layer,
                        evidence=RuleEvidence(
                            features={
                                "issue": "undefined_acronym",
                                "acronym": acronym,
                                "full_form": None,
                                "acronym_mentions": len(sentence_mentions),
                                "full_form_mentions": 0,
                            },
                        ),
                        confidence=0.9,
                        rationale=(
                            "Undefined-acronym detection anchors to first mention order and "
                            "definition pattern extraction."
                        ),
                        rewrite_tactics=(
                            "Introduce the full term before the acronym and keep the acronym as a secondary shorthand.",
                        ),
                    )
                )
                continue

            acronym_mentions = len(sentence_mentions)
            full_form_mentions = _count_full_form_mentions(doc, definition.full_form)
            if acronym_mentions < min_mentions_for_overuse:
                continue
            ratio = (
                float("inf") if full_form_mentions == 0 else acronym_mentions / full_form_mentions
            )
            if ratio <= max_ratio:
                continue
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    message=(
                        f"Acronym '{acronym}' dominates its full form '{definition.full_form}' "
                        "in running prose."
                    ),
                    span=first_sentence.span,
                    severity=self.settings.severity,
                    layer=self.metadata.layer,
                    evidence=RuleEvidence(
                        features={
                            "issue": "acronym_overuse",
                            "acronym": acronym,
                            "full_form": definition.full_form,
                            "acronym_mentions": acronym_mentions,
                            "full_form_mentions": full_form_mentions,
                        },
                        score=ratio if ratio != float("inf") else None,
                        threshold=max_ratio,
                    ),
                    confidence=0.78,
                    rationale=(
                        "Acronym-overuse detection compares acronym mentions against full-form "
                        "mentions after a valid local definition is available."
                    ),
                    rewrite_tactics=(
                        "Keep the full form as the dominant reference in prose and reserve the acronym for dense local contexts.",
                    ),
                )
            )
        return violations


def _collect_mentions(
    doc,
    allowlist: frozenset[str],
    ordinal_by_sentence_id: dict[str, int],
) -> dict[str, list[tuple[int, Sentence]]]:
    mentions: dict[str, list[tuple[int, Sentence]]] = {}
    for sentence in iter_sentences(doc):
        ordinal = ordinal_by_sentence_id.get(sentence.id, 10**9)
        for match in ACRONYM_RE.finditer(sentence.source_text):
            acronym = _normalize_acronym(match.group(0))
            if acronym in allowlist:
                continue
            mentions.setdefault(acronym, []).append((ordinal, sentence))
    for acronym, rows in mentions.items():
        rows.sort(key=lambda item: (item[0], item[1].span.start))
        mentions[acronym] = rows
    return mentions


def _collect_definitions(
    doc,
    allowlist: frozenset[str],
    ordinal_by_sentence_id: dict[str, int],
    definition_stopwords: frozenset[str],
) -> dict[str, AcronymDefinition]:
    definitions: dict[str, AcronymDefinition] = {}
    for sentence in iter_sentences(doc):
        ordinal = ordinal_by_sentence_id.get(sentence.id, 10**9)
        for match in FULL_FORM_THEN_ACRONYM_RE.finditer(sentence.source_text):
            definition = _definition_from_match(
                match.group("acronym"),
                match.group("full"),
                sentence.id,
                ordinal,
                definition_stopwords,
            )
            if definition is None or definition.acronym in allowlist:
                continue
            _store_definition(definitions, definition)
        for match in ACRONYM_THEN_FULL_FORM_RE.finditer(sentence.source_text):
            definition = _definition_from_match(
                match.group("acronym"),
                match.group("full"),
                sentence.id,
                ordinal,
                definition_stopwords,
            )
            if definition is None or definition.acronym in allowlist:
                continue
            _store_definition(definitions, definition)
    return definitions


def _definition_from_match(
    acronym_raw: str,
    full_form_raw: str,
    sentence_id: str,
    sentence_ordinal: int,
    definition_stopwords: frozenset[str],
) -> AcronymDefinition | None:
    acronym = _normalize_acronym(acronym_raw)
    full_form = _normalize_full_form(full_form_raw)
    if not acronym or not full_form:
        return None
    if not _initials_align(acronym, full_form, definition_stopwords):
        return None
    return AcronymDefinition(
        acronym=acronym,
        full_form=full_form,
        sentence_id=sentence_id,
        sentence_ordinal=sentence_ordinal,
    )


def _store_definition(
    definitions: dict[str, AcronymDefinition],
    definition: AcronymDefinition,
) -> None:
    current = definitions.get(definition.acronym)
    if current is None or definition.sentence_ordinal < current.sentence_ordinal:
        definitions[definition.acronym] = definition


def _normalize_acronym(value: str) -> str:
    acronym = value.strip()
    if acronym.endswith("s") and len(acronym) > 2:
        acronym = acronym[:-1]
    return acronym


def _normalize_full_form(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip())


def _initials_align(
    acronym: str,
    full_form: str,
    definition_stopwords: frozenset[str],
) -> bool:
    words = [word.group(0) for word in WORD_RE.finditer(full_form)]
    if len(words) < 2:
        return False
    initials = "".join(
        word[0].upper() for word in words if word.lower() not in definition_stopwords
    )
    if not initials:
        return False
    if initials.startswith(acronym):
        return True
    shared_prefix = 0
    for acronym_char, initial_char in zip(acronym, initials, strict=False):
        if acronym_char != initial_char:
            break
        shared_prefix += 1
    return shared_prefix >= max(2, int(len(acronym) * 0.6))


def _count_full_form_mentions(doc, full_form: str) -> int:
    pattern = re.compile(rf"\b{re.escape(full_form)}\b", re.IGNORECASE)
    count = 0
    for sentence in iter_sentences(doc):
        count += len(pattern.findall(sentence.source_text))
    return count


def register(registry) -> None:
    registry.add(AcronymBurdenRule)
