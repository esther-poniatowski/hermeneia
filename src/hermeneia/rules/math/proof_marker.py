"""Proof-marker placement checks."""

from __future__ import annotations

import re

from hermeneia.document.model import Span
from hermeneia.rules.base import (
    Layer,
    RuleEvidence,
    RuleKind,
    RuleMetadata,
    Severity,
    SourcePatternRule,
    Tractability,
    Violation,
)

PROOF_OPENER_RE = re.compile(r"^\s*(?:\*?Proof\.?\*?)\s*$", re.IGNORECASE)
PROOF_END_RE = re.compile(r"(?:\$?\\square\$?|□|QED)\s*$", re.IGNORECASE)


class ProofMarkerRule(SourcePatternRule):
    metadata = RuleMetadata(
        rule_id="math.proof_marker",
        label="Proof end markers require explicit proof opener",
        layer=Layer.SURFACE_STYLE,
        tractability=Tractability.CLASS_A,
        kind=RuleKind.HARD_CONSTRAINT,
        default_severity=Severity.ERROR,
        supported_languages=frozenset({"en"}),
        default_options={"max_lookback_lines": 12},
        evidence_fields=("end_marker", "has_proof_opener"),
    )

    def check_source(self, lines, doc, ctx):
        _ = doc, ctx
        max_lookback = self.settings.int_option("max_lookback_lines", 12)
        violations: list[Violation] = []
        for index, line in enumerate(lines):
            if PROOF_END_RE.search(line.text.strip()) is None:
                continue
            start = max(0, index - max_lookback)
            window = lines[start:index]
            has_proof_opener = any(
                PROOF_OPENER_RE.match(candidate.text.strip()) for candidate in window
            )
            if has_proof_opener:
                continue
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    message="Proof ending marker appears without a preceding 'Proof.' opener.",
                    span=_line_span(line),
                    severity=self.settings.severity,
                    layer=self.metadata.layer,
                    evidence=RuleEvidence(
                        features={
                            "end_marker": line.text.strip(),
                            "has_proof_opener": has_proof_opener,
                        }
                    ),
                    rewrite_tactics=(
                        "Introduce '*Proof.*' before the proof body when using a closing square marker.",
                    ),
                )
            )
        return violations


def _line_span(line) -> Span:
    return Span(
        start=line.span.start,
        end=line.span.end,
        start_line=line.span.start_line,
        start_column=line.span.start_column,
        end_line=line.span.end_line,
        end_column=line.span.end_column,
    )


def register(registry) -> None:
    registry.add(ProofMarkerRule)
