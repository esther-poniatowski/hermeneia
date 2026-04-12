"""First-use definition checks for mathematical symbols."""

from __future__ import annotations

import re

from hermeneia.document.indexes import SupportSignalKind
from hermeneia.document.model import BlockKind, Sentence
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
from hermeneia.rules.common import (
    iter_blocks,
    matched_sentence_markers,
    upstream_limits,
)

INLINE_SYMBOL_RE = re.compile(r"^\$([A-Za-z][A-Za-z0-9']*)\$$")
MATH_LET_MARKER_RE = re.compile(r"\blet\s+\$?[A-Za-z][A-Za-z0-9']*\$?\b", re.IGNORECASE)
GENERIC_DEFINITION_CUE_RE = re.compile(
    r"\b(?:define|definition|notation|write|set|introduce)\b", re.IGNORECASE
)
COMMA_SEPARATOR = ", "


class DefinitionBeforeUseRule(HeuristicSemanticRule):
    """Definitionbeforeuserule."""

    metadata = RuleMetadata(
        rule_id="terminology.definition_before_use",
        label="First-use symbols should be defined in place",
        layer=Layer.AUDIENCE_FIT,
        tractability=Tractability.CLASS_H,
        kind=RuleKind.SOFT_HEURISTIC,
        default_severity=Severity.INFO,
        supported_languages=frozenset({"en"}),
        abstain_when_flags=frozenset(
            {"heavy_math_masking", "symbol_dense_sentence", "fragment_sentence"}
        ),
        evidence_fields=("symbols", "matched_markers", "definition_signals"),
    )

    def check(self, doc, ctx):
        """Check."""
        definitional_markers = tuple(
            marker.lower() for marker in ctx.language_pack.lexicons.definitional_markers
        )
        violations: list[Violation] = []
        definition_signal_sentences = {
            signal.sentence_id
            for signal in doc.indexes.support_signals
            if signal.kind == SupportSignalKind.DEFINITION_MARKER
            and signal.sentence_id is not None
        }
        for block in iter_blocks(
            doc,
            {
                BlockKind.HEADING,
                BlockKind.PARAGRAPH,
                BlockKind.LIST_ITEM,
                BlockKind.TABLE_CELL,
                BlockKind.BLOCK_QUOTE,
                BlockKind.ADMONITION,
                BlockKind.FOOTNOTE,
            },
        ):
            for index, sentence in enumerate(block.sentences):
                if self.should_abstain(sentence.annotation_flags):
                    continue
                previous_sentence = block.sentences[index - 1] if index > 0 else None
                sentence_matched_markers = matched_sentence_markers(
                    sentence, definitional_markers
                )
                undefined_symbols: set[str] = set()
                matched_markers: set[str] = set()
                definition_signals: set[str] = set()
                for node in sentence.inline_nodes:
                    symbol_match = INLINE_SYMBOL_RE.fullmatch(node.text.strip())
                    if symbol_match is None:
                        continue
                    symbol = symbol_match.group(1)
                    first_use_span = ctx.features.symbol_first_use(symbol)
                    if first_use_span != node.span:
                        continue
                    signal = _definition_signal_for_symbol(
                        symbol=symbol,
                        sentence=sentence,
                        previous_sentence=previous_sentence,
                        sentence_markers=sentence_matched_markers,
                        definition_signal_sentences=definition_signal_sentences,
                    )
                    if signal is None:
                        undefined_symbols.add(symbol)
                        continue
                    definition_signals.update(signal)
                    matched_markers.update(sentence_matched_markers)

                if not undefined_symbols:
                    continue
                symbols = tuple(sorted(undefined_symbols))
                violations.append(
                    Violation(
                        rule_id=self.rule_id,
                        message=(
                            "Introduce and define symbol(s) "
                            f"{COMMA_SEPARATOR.join(symbols)} at first use."
                        ),
                        span=sentence.span,
                        severity=self.settings.severity,
                        layer=self.metadata.layer,
                        evidence=RuleEvidence(
                            features={
                                "symbols": symbols,
                                "matched_markers": tuple(sorted(matched_markers)),
                                "definition_signals": tuple(sorted(definition_signals)),
                            },
                            upstream_limits=upstream_limits(sentence),
                        ),
                        confidence=0.7,
                        rationale=(
                            "Definition-before-use uses first-use span identity plus local "
                            "definition signatures (markers, assignment forms, and symbol-binding "
                            "patterns) to remain evidence-based."
                        ),
                        rewrite_tactics=(
                            "Add a brief local definition immediately at the first mention of each symbol.",
                        ),
                    )
                )
        return violations


def _definition_signal_for_symbol(
    symbol: str,
    sentence: Sentence,
    previous_sentence: Sentence | None,
    sentence_markers: tuple[str, ...],
    definition_signal_sentences: set[str],
) -> tuple[str, ...] | None:
    """Definition signal for symbol."""
    sentence_text = sentence.source_text
    signals: set[str] = set()
    for marker in sentence_markers:
        signals.add(f"marker:{marker}")
    if MATH_LET_MARKER_RE.search(sentence_text):
        signals.add("let_binding")

    symbol_pattern = re.escape(symbol)
    inline_symbol = rf"\$?{symbol_pattern}\$?"
    direct_patterns = {
        "assignment": re.compile(rf"{inline_symbol}\s*(?::=|=)\s*", re.IGNORECASE),
        "where_with_binding": re.compile(
            rf"\b(?:where|with)\s+{inline_symbol}\s+"
            r"(?:is|are|means|denotes|refers to|represents|measures|is\s+defined\s+as)\b",
            re.IGNORECASE,
        ),
        "symbol_copula_noun_phrase": re.compile(
            rf"{inline_symbol}\s+(?:is|are)\s+(?:the|a|an)\b",
            re.IGNORECASE,
        ),
        "symbol_copula_colon": re.compile(
            rf"{inline_symbol}\s+(?:is|are)\s*:\s*",
            re.IGNORECASE,
        ),
        "copula_colon_to_symbol": re.compile(
            rf"\b(?:is|are)\s*:\s*{inline_symbol}\b",
            re.IGNORECASE,
        ),
        "term_to_symbol": re.compile(
            rf"\b(?:is|are|denoted\s+by|written\s+as|measured\s+by)\s+{inline_symbol}\b",
            re.IGNORECASE,
        ),
    }
    for signal_name, pattern in direct_patterns.items():
        if pattern.search(sentence_text):
            signals.add(signal_name)

    if sentence.id in definition_signal_sentences:
        signals.add("support_signal:definition_marker")

    if previous_sentence is not None:
        previous_lower = previous_sentence.source_text.lower()
        if GENERIC_DEFINITION_CUE_RE.search(previous_lower):
            if direct_patterns["assignment"].search(sentence_text) or direct_patterns[
                "symbol_copula_colon"
            ].search(sentence_text):
                signals.add("carryover_definition_frame")
        if previous_sentence.id in definition_signal_sentences:
            if direct_patterns["assignment"].search(sentence_text) or direct_patterns[
                "term_to_symbol"
            ].search(sentence_text):
                signals.add("carryover_definition_signal")

    if not signals:
        return None
    return tuple(sorted(signals))


def register(registry) -> None:
    """Register."""
    registry.add(DefinitionBeforeUseRule)
