"""Detect boilerplate sentence openers that delay the key claim."""

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
from hermeneia.rules.common import iter_sentences
from hermeneia.rules.patterns import compile_leading_phrase_regex


class BoilerplateOpenerRule(AnnotatedRule):
    """Boilerplateopenerrule."""

    metadata = RuleMetadata(
        rule_id="vocabulary.boilerplate_opener",
        label="Avoid boilerplate openers in declarative prose",
        layer=Layer.SURFACE_STYLE,
        tractability=Tractability.CLASS_A,
        kind=RuleKind.SOFT_HEURISTIC,
        default_severity=Severity.WARNING,
        supported_languages=frozenset({"en"}),
        evidence_fields=("opener",),
    )

    def check(self, doc, ctx):
        """Check."""
        patterns = list(ctx.language_pack.lexicons.boilerplate_openers) + list(
            self.settings.extra_patterns
        )
        silenced = {item.lower() for item in self.settings.silenced_patterns}
        filtered = tuple(
            item.strip()
            for item in patterns
            if item.strip() and item.strip().lower() not in silenced
        )
        regex = compile_leading_phrase_regex(filtered)
        violations: list[Violation] = []
        for sentence in iter_sentences(doc):
            match = regex.search(sentence.projection.text)
            if match is None:
                continue
            opener = match.group(0).strip().lower()
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    message=(
                        f"Sentence opens with boilerplate framing '{opener}'; "
                        "state the concrete claim directly."
                    ),
                    span=sentence.span,
                    severity=self.settings.severity,
                    layer=self.metadata.layer,
                    evidence=RuleEvidence(features={"opener": opener}),
                    rewrite_tactics=(
                        "Start the sentence with the operative claim, result, or mechanism.",
                    ),
                )
            )
        return violations


def register(registry) -> None:
    """Register."""
    registry.add(BoilerplateOpenerRule)
