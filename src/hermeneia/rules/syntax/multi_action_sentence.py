"""Detect sentences that stack multiple load-bearing actions."""

from __future__ import annotations

import re

from hermeneia.document.model import Token
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
from hermeneia.rules.patterns import compile_inline_phrase_regex

VERB_DEP_BLACKLIST = frozenset({"aux", "auxpass", "mark", "cop"})
VERB_DEP_ALLOW_PREFIXES = ("root", "conj", "ccomp", "xcomp", "advcl")


class MultiActionSentenceRule(AnnotatedRule):
    """Multiactionsentencerule."""

    metadata = RuleMetadata(
        rule_id="syntax.multi_action_sentence",
        label="Keep one primary action per sentence",
        layer=Layer.LOCAL_DISCOURSE,
        tractability=Tractability.CLASS_B,
        kind=RuleKind.SOFT_HEURISTIC,
        default_severity=Severity.WARNING,
        supported_languages=frozenset({"en"}),
        default_options={
            "max_load_bearing_verbs": 1,
            "require_coordination_marker": True,
            "apply_block_kinds": ("paragraph",),
            "coordination_markers": ("and", "while", "whereas", "then", ";"),
        },
        abstain_when_flags=frozenset(
            {
                "heavy_math_masking",
                "symbol_dense_sentence",
                "fragment_sentence",
                "list_item_context",
                "blockquote_context",
                "table_cell_context",
                "heading_context",
            }
        ),
        evidence_fields=("action_count", "verbs", "coordination_signal"),
    )

    def check(self, doc, ctx):
        """Check."""
        max_actions = self.settings.int_option("max_load_bearing_verbs", 1)
        require_marker = self.settings.bool_option("require_coordination_marker", True)
        weak_support_verbs = ctx.language_pack.lexicons.weak_support_verbs
        configured_markers = self.settings.options.get("coordination_markers")
        connector_terms: tuple[str, ...]
        if isinstance(configured_markers, str):
            connector_terms = (configured_markers,)
        elif isinstance(configured_markers, (list, tuple)):
            connector_terms = tuple(
                marker
                for marker in configured_markers
                if isinstance(marker, str) and marker.strip()
            )
        else:
            connector_terms = ("and", "while", "whereas", "then", ";")
        connector_pattern, semicolon_signal = _compile_connector_pattern(connector_terms)
        violations: list[Violation] = []
        for sentence in iter_sentences(doc):
            if self.should_abstain(sentence.annotation_flags):
                continue
            verbs = _load_bearing_verbs(sentence.tokens, weak_support_verbs)
            if len(verbs) <= max_actions:
                continue
            has_coordination_signal = _has_coordination_signal(
                sentence.projection.text,
                connector_pattern=connector_pattern,
                semicolon_signal=semicolon_signal,
            )
            if require_marker and not has_coordination_signal:
                continue
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    message=(
                        "Sentence appears to carry multiple load-bearing actions; "
                        "split it so each sentence advances one main action."
                    ),
                    span=sentence.span,
                    severity=self.settings.severity,
                    layer=self.metadata.layer,
                    evidence=RuleEvidence(
                        features={
                            "action_count": len(verbs),
                            "verbs": tuple(verbs),
                            "coordination_signal": has_coordination_signal,
                        },
                        threshold=float(max_actions),
                        upstream_limits=upstream_limits(sentence),
                    ),
                    confidence=0.76 if has_coordination_signal else 0.65,
                    rationale=(
                        "The heuristic counts load-bearing verbal heads and checks whether "
                        "coordination markers stack multiple actions in one sentence."
                    ),
                    rewrite_tactics=(
                        "Split the sentence so each clause carries one primary claim or operation.",
                    ),
                )
            )
        return violations


def _load_bearing_verbs(
    tokens: list[Token],
    weak_support_verbs: frozenset[str],
) -> tuple[str, ...]:
    """Load-bearing verbs."""
    if not tokens:
        return ()
    collected: list[str] = []
    seen_spans: set[tuple[int, int]] = set()
    for token in tokens:
        pos = (token.pos or "").upper()
        if pos not in {"VERB", "AUX"}:
            continue
        lemma = (token.lemma or token.text).lower()
        if lemma in weak_support_verbs:
            continue
        dep = (token.dep or "").lower()
        if dep in VERB_DEP_BLACKLIST:
            continue
        if dep and not dep.startswith(VERB_DEP_ALLOW_PREFIXES):
            continue
        span_key = (token.source_span.start, token.source_span.end)
        if span_key in seen_spans:
            continue
        seen_spans.add(span_key)
        collected.append(token.text.lower())
    return tuple(collected)


def _compile_connector_pattern(
    connector_terms: tuple[str, ...],
) -> tuple[re.Pattern[str], bool]:
    """Compile connector pattern."""
    words = tuple(term for term in connector_terms if term.strip() and term.strip() != ";")
    pattern = compile_inline_phrase_regex(words)
    return pattern, ";" in connector_terms


def _has_coordination_signal(
    text: str,
    *,
    connector_pattern: re.Pattern[str],
    semicolon_signal: bool,
) -> bool:
    """Has coordination signal."""
    if semicolon_signal and ";" in text:
        return True
    return connector_pattern.search(text) is not None


def register(registry) -> None:
    """Register."""
    registry.add(MultiActionSentenceRule)
