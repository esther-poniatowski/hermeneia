"""First-person and generic pronoun checks for formal prose."""

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
from hermeneia.rules.common import iter_sentences, match_allowed
from hermeneia.rules.patterns import compile_inline_phrase_regex

SUBJECT_DEPENDENCIES = frozenset({"nsubj", "nsubjpass", "csubj"})


class PronounRule(AnnotatedRule):
    metadata = RuleMetadata(
        rule_id="surface.pronoun",
        label="Avoid first-person or generic-pronoun scaffolding",
        layer=Layer.SURFACE_STYLE,
        tractability=Tractability.CLASS_B,
        kind=RuleKind.SOFT_HEURISTIC,
        default_severity=Severity.INFO,
        supported_languages=frozenset({"en"}),
        evidence_fields=("pronoun", "signal"),
    )

    def check(self, doc, ctx):
        pronoun_pattern = compile_inline_phrase_regex(
            tuple(ctx.language_pack.lexicons.pronoun_scaffolding_markers)
        )
        violations: list[Violation] = []
        seen_spans: set[tuple[int, int]] = set()

        for line in doc.source_lines:
            if any(kind.value in {"code_block", "display_math"} for kind in line.container_kinds):
                continue
            match = match_allowed(line, pronoun_pattern)
            if match is None:
                continue
            span = _line_match_span(line, match.start(), match.end())
            if _seen(seen_spans, span.start, span.end):
                continue
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    message=(
                        "Prefer object-centered phrasing over first-person or generic-pronoun "
                        "scaffolding."
                    ),
                    span=span,
                    severity=self.settings.severity,
                    layer=self.metadata.layer,
                    evidence=RuleEvidence(
                        features={"pronoun": match.group(0).lower(), "signal": "phrase_match"}
                    ),
                    confidence=0.7,
                    rewrite_tactics=(
                        "Name the operation, statement, or object directly instead of using a generic actor.",
                    ),
                )
            )

        for sentence in iter_sentences(doc):
            token = _subject_one_token(sentence.tokens)
            if token is None:
                continue
            if _seen(seen_spans, token.source_span.start, token.source_span.end):
                continue
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    message=(
                        "Avoid generic subject 'one' in formal exposition; name the object or "
                        "agent directly."
                    ),
                    span=token.source_span,
                    severity=self.settings.severity,
                    layer=self.metadata.layer,
                    evidence=RuleEvidence(
                        features={
                            "pronoun": "one",
                            "signal": "subject_dependency",
                            "dependency": (token.dep or "").lower(),
                        }
                    ),
                    confidence=0.8,
                    rewrite_tactics=(
                        "Rewrite with an explicit subject, object, or statement-centered construction.",
                    ),
                )
            )
        return violations


def _line_match_span(line, start: int, end: int):
    return line.span.__class__(
        start=line.span.start + start,
        end=line.span.start + end,
        start_line=line.span.start_line,
        start_column=line.span.start_column + start,
        end_line=line.span.start_line,
        end_column=line.span.start_column + end,
    )


def _subject_one_token(tokens):
    for token in tokens:
        lemma = (token.lemma or token.text).lower()
        dependency = (token.dep or "").lower()
        if lemma != "one":
            continue
        if dependency in SUBJECT_DEPENDENCIES:
            return token
    return None


def _seen(seen_spans: set[tuple[int, int]], start: int, end: int) -> bool:
    key = (start, end)
    if key in seen_spans:
        return True
    seen_spans.add(key)
    return False


def register(registry) -> None:
    registry.add(PronounRule)
