"""Acronym burden and first-use density checks."""

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

ACRONYM_RE = re.compile(r"\b[A-Z]{2,}(?:s)?\b")


class AcronymBurdenRule(AnnotatedRule):
    metadata = RuleMetadata(
        rule_id="audience.acronym_burden",
        label="Acronym burden is too high for the surrounding sentence",
        layer=Layer.AUDIENCE_FIT,
        tractability=Tractability.CLASS_A,
        kind=RuleKind.SOFT_HEURISTIC,
        default_severity=Severity.WARNING,
        supported_languages=frozenset({"en"}),
        default_options={"max_distinct_acronyms": 2},
        evidence_fields=("acronyms",),
    )

    def check(self, doc, ctx):
        max_distinct = self.settings.int_option("max_distinct_acronyms", 2)
        allowlist = ctx.language_pack.lexicons.acronym_allowlist
        violations: list[Violation] = []
        for sentence in iter_sentences(doc):
            acronyms = {
                match.group(0)
                for match in ACRONYM_RE.finditer(sentence.source_text)
                if match.group(0) not in allowlist
            }
            if len(acronyms) <= max_distinct:
                continue
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    message=f"Sentence introduces {len(acronyms)} distinct acronyms ({', '.join(sorted(acronyms))}).",
                    span=sentence.span,
                    severity=self.settings.severity,
                    layer=self.metadata.layer,
                    evidence=RuleEvidence(
                        features={"acronyms": tuple(sorted(acronyms))},
                        threshold=float(max_distinct),
                    ),
                    rewrite_tactics=(
                        "Define acronyms at first use and reduce the number introduced in a single sentence.",
                    ),
                )
            )
        return violations


def register(registry) -> None:
    registry.add(AcronymBurdenRule)
