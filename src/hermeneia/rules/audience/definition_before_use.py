"""First-use definition checks for mathematical symbols."""

from __future__ import annotations

import re

from hermeneia.rules.base import (
    HeuristicSemanticRule,
    Layer,
    RuleEvidence,
    RuleKind,
    RuleMetadata,
    Severity,
    Tractability,
    Violation,
)
from hermeneia.rules.common import iter_sentences, upstream_limits

INLINE_SYMBOL_RE = re.compile(r"^\$([A-Za-z][A-Za-z0-9']*)\$$")
MATH_LET_MARKER_RE = re.compile(r"\blet\s+\$?[A-Za-z][A-Za-z0-9']*\$?\b", re.IGNORECASE)


class DefinitionBeforeUseRule(HeuristicSemanticRule):
    metadata = RuleMetadata(
        rule_id="audience.definition_before_use",
        label="First-use symbols should be defined in place",
        layer=Layer.AUDIENCE_FIT,
        tractability=Tractability.CLASS_H,
        kind=RuleKind.SOFT_HEURISTIC,
        default_severity=Severity.INFO,
        supported_languages=frozenset({"en"}),
        abstain_when_flags=frozenset(
            {"heavy_math_masking", "symbol_dense_sentence", "fragment_sentence"}
        ),
        evidence_fields=("symbols", "has_definition_marker", "matched_markers"),
    )

    def check(self, doc, ctx):
        definitional_markers = tuple(
            marker.lower() for marker in ctx.language_pack.lexicons.definitional_markers
        )
        violations: list[Violation] = []
        for sentence in iter_sentences(doc):
            if self.should_abstain(sentence.annotation_flags):
                continue
            lowered = sentence.source_text.lower()
            matched_markers = tuple(marker for marker in definitional_markers if marker in lowered)
            has_definition_marker = bool(matched_markers) or bool(
                MATH_LET_MARKER_RE.search(sentence.source_text)
            )

            undefined_symbols: set[str] = set()
            for node in sentence.inline_nodes:
                symbol_match = INLINE_SYMBOL_RE.fullmatch(node.text.strip())
                if symbol_match is None:
                    continue
                symbol = symbol_match.group(1)
                first_use_span = ctx.features.symbol_first_use(symbol)
                if first_use_span != node.span:
                    continue
                if has_definition_marker:
                    continue
                undefined_symbols.add(symbol)

            if not undefined_symbols:
                continue
            symbols = tuple(sorted(undefined_symbols))
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    message=f"Introduce and define symbol(s) {', '.join(symbols)} at first use.",
                    span=sentence.span,
                    severity=self.settings.severity,
                    layer=self.metadata.layer,
                    evidence=RuleEvidence(
                        features={
                            "symbols": symbols,
                            "has_definition_marker": has_definition_marker,
                            "matched_markers": matched_markers,
                        },
                        upstream_limits=upstream_limits(sentence),
                    ),
                    confidence=0.7,
                    rationale="Definition-before-use is a bounded first-use heuristic grounded in parser spans and local marker checks.",
                    rewrite_tactics=(
                        "Add a brief local definition immediately at the first mention of each symbol.",
                    ),
                )
            )
        return violations


def register(registry) -> None:
    registry.add(DefinitionBeforeUseRule)
