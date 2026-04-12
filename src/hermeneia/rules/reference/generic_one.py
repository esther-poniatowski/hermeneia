"""Hard rule for generic-actor 'one' scaffolding."""

from __future__ import annotations

from hermeneia.document.model import BlockKind, Span, Token
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
from hermeneia.rules.common import line_text_outside_excluded
from hermeneia.rules.patterns import compile_inline_phrase_regex

SUBJECT_DEPENDENCIES = frozenset({"nsubj", "nsubjpass", "csubj"})

PROSE_BLOCK_KINDS = {
    BlockKind.HEADING,
    BlockKind.PARAGRAPH,
    BlockKind.LIST_ITEM,
    BlockKind.BLOCK_QUOTE,
    BlockKind.TABLE_CELL,
    BlockKind.FOOTNOTE,
    BlockKind.ADMONITION,
}


class GenericOneRule(AnnotatedRule):
    """Genericonerule."""

    metadata = RuleMetadata(
        rule_id="reference.generic_one",
        label="Avoid generic actor 'one' in technical prose",
        layer=Layer.SURFACE_STYLE,
        tractability=Tractability.CLASS_B,
        kind=RuleKind.HARD_CONSTRAINT,
        default_severity=Severity.ERROR,
        supported_languages=frozenset({"en"}),
        evidence_fields=("signal", "phrase"),
    )

    def check(self, doc, ctx):
        """Check."""
        markers = tuple(ctx.language_pack.lexicons.generic_one_markers)
        phrase_markers = tuple(marker for marker in markers if " " in marker)
        phrase_pattern = compile_inline_phrase_regex(phrase_markers)
        violations: list[Violation] = []
        seen_spans: set[tuple[int, int]] = set()

        for line in doc.source_lines:
            if not _is_prose_line(line):
                continue
            probe = line_text_outside_excluded(line)
            for match in phrase_pattern.finditer(probe):
                span = _match_span(line, match.start(), match.end())
                if _seen(seen_spans, span):
                    continue
                phrase = match.group(0).lower()
                violations.append(
                    Violation(
                        rule_id=self.rule_id,
                        message=(
                            f"Replace generic actor phrase '{phrase}' with an explicit "
                            "subject or object-centered construction."
                        ),
                        span=span,
                        severity=self.settings.severity,
                        layer=self.metadata.layer,
                        evidence=RuleEvidence(
                            features={"signal": "phrase_match", "phrase": phrase}
                        ),
                        confidence=0.86,
                        rewrite_tactics=(
                            "Name the concrete object, operation, or agent instead of using generic 'one'.",
                        ),
                    )
                )

        for block in doc.iter_blocks():
            if block.kind not in PROSE_BLOCK_KINDS:
                continue
            for sentence in block.sentences:
                token = _subject_one_token(sentence.tokens)
                if token is None:
                    continue
                if _seen(seen_spans, token.source_span):
                    continue
                violations.append(
                    Violation(
                        rule_id=self.rule_id,
                        message=(
                            "Avoid generic subject 'one'; rewrite with an explicit "
                            "subject, object, or claim-centered form."
                        ),
                        span=token.source_span,
                        severity=self.settings.severity,
                        layer=self.metadata.layer,
                        evidence=RuleEvidence(
                            features={
                                "signal": "subject_dependency",
                                "phrase": "one",
                                "dependency": (token.dep or "").lower(),
                            }
                        ),
                        confidence=0.92,
                        rewrite_tactics=(
                            "Replace 'one' with the concrete entity performing the action.",
                        ),
                    )
                )
        return violations


def _subject_one_token(tokens: list[Token]) -> Token | None:
    """Subject one token."""
    for token in tokens:
        lemma = (token.lemma or token.text).lower()
        dependency = (token.dep or "").lower()
        if lemma == "one" and dependency in SUBJECT_DEPENDENCIES:
            return token
    return None


def _is_prose_line(line) -> bool:
    """Is prose line."""
    if not line.container_kinds:
        return True
    if any(
        kind in {BlockKind.CODE_BLOCK, BlockKind.DISPLAY_MATH}
        for kind in line.container_kinds
    ):
        return False
    return any(kind in PROSE_BLOCK_KINDS for kind in line.container_kinds)


def _match_span(line, start: int, end: int) -> Span:
    """Match span."""
    return Span(
        start=line.span.start + start,
        end=line.span.start + end,
        start_line=line.span.start_line,
        start_column=line.span.start_column + start,
        end_line=line.span.start_line,
        end_column=line.span.start_column + end,
    )


def _seen(seen: set[tuple[int, int]], span: Span) -> bool:
    """Seen."""
    key = (span.start, span.end)
    if key in seen:
        return True
    seen.add(key)
    return False


def register(registry) -> None:
    """Register."""
    registry.add(GenericOneRule)
