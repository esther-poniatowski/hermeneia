"""Discourse-transition articulation heuristics."""

from __future__ import annotations

import re
from dataclasses import dataclass

from hermeneia.document.model import BlockKind
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
from hermeneia.rules.common import iter_blocks
from hermeneia.rules.patterns import (
    compile_inline_phrase_regex,
    compile_leading_phrase_regex,
    compile_prefixed_term_regex,
)

WORD_RE = re.compile(r"\b[a-z][a-z-]*\b", re.IGNORECASE)
INITIAL_IF_BOUNDARY_RE = re.compile(
    r"^\s*if\b(?P<condition>.*?)(?:[,;:])(?P<rest>.*)$", re.IGNORECASE
)


@dataclass(frozen=True)
class _TransitionConfig:
    """Resolved runtime parameters for transition-quality checks."""

    min_overlap: float
    max_shift_findings: int
    min_paragraph_sentences: int
    min_average_overlap: float
    detect_if_without_then: bool
    max_if_without_then_findings: int
    detect_implicit_contrast: bool
    max_implicit_contrast_findings: int
    min_overlap_for_implicit_contrast: float
    connector_pattern: re.Pattern[str]
    explicit_contrast_pattern: re.Pattern[str]
    reference_pattern: re.Pattern[str]
    conditional_markers: frozenset[str]
    positive_contrast_terms: frozenset[str]
    negative_contrast_terms: frozenset[str]


class TransitionQualityRule(HeuristicSemanticRule):
    """Transitionqualityrule."""

    metadata = RuleMetadata(
        rule_id="linkage.transition_quality",
        label="Discourse transitions are weakly articulated",
        layer=Layer.LOCAL_DISCOURSE,
        tractability=Tractability.CLASS_H,
        kind=RuleKind.DIAGNOSTIC_METRIC,
        default_severity=Severity.INFO,
        supported_languages=frozenset({"en"}),
        default_options={
            "apply_block_kinds": ("paragraph",),
            "min_overlap_without_connector": 0.18,
            "max_shift_findings": 3,
            "min_paragraph_sentences": 4,
            "min_average_overlap_without_connectors": 0.35,
            "detect_if_without_then": True,
            "max_if_without_then_findings": 3,
            "detect_implicit_contrast": True,
            "max_implicit_contrast_findings": 3,
            "min_overlap_for_implicit_contrast": 0.2,
        },
        evidence_fields=("issue",),
    )

    def check(self, doc, ctx):
        """Check.

        Parameters
        ----------
        doc : object
            Document instance to inspect.
        ctx : object
            Rule evaluation context.

        Returns
        -------
        object
            Resulting value produced by this call.
        """
        config = _build_transition_config(self, ctx)
        violations: list[Violation] = []
        for block in iter_blocks(doc, {BlockKind.PARAGRAPH}):
            if _block_in_structured_context(block):
                continue
            violations.extend(_if_without_then_violations(self, block, config))
            violations.extend(_implicit_contrast_violations(self, block, ctx, config))
            violations.extend(_unmarked_shift_violations(self, block, ctx, config))
        return violations


def _build_transition_config(rule: TransitionQualityRule, ctx) -> _TransitionConfig:
    """Build resolved transition-quality configuration."""
    return _TransitionConfig(
        min_overlap=rule.settings.float_option("min_overlap_without_connector", 0.18),
        max_shift_findings=rule.settings.int_option("max_shift_findings", 3),
        min_paragraph_sentences=rule.settings.int_option("min_paragraph_sentences", 4),
        min_average_overlap=rule.settings.float_option(
            "min_average_overlap_without_connectors", 0.35
        ),
        detect_if_without_then=rule.settings.bool_option("detect_if_without_then", True),
        max_if_without_then_findings=rule.settings.int_option("max_if_without_then_findings", 3),
        detect_implicit_contrast=rule.settings.bool_option("detect_implicit_contrast", True),
        max_implicit_contrast_findings=rule.settings.int_option(
            "max_implicit_contrast_findings", 3
        ),
        min_overlap_for_implicit_contrast=rule.settings.float_option(
            "min_overlap_for_implicit_contrast", 0.2
        ),
        connector_pattern=compile_leading_phrase_regex(
            tuple(ctx.language_pack.lexicons.transition_connectors)
        ),
        explicit_contrast_pattern=compile_inline_phrase_regex(
            tuple(ctx.language_pack.lexicons.explicit_contrast_markers)
        ),
        reference_pattern=compile_prefixed_term_regex(
            ("this", "these", "that", "such"),
            tuple(ctx.language_pack.lexicons.transition_reference_heads),
            anchored=True,
        ),
        conditional_markers=frozenset(
            marker.lower() for marker in ctx.language_pack.lexicons.conditional_consequence_markers
        ),
        positive_contrast_terms=frozenset(
            term.lower() for term in ctx.language_pack.lexicons.contrast_polarity_positive_terms
        ),
        negative_contrast_terms=frozenset(
            term.lower() for term in ctx.language_pack.lexicons.contrast_polarity_negative_terms
        ),
    )


def _if_without_then_violations(
    rule: TransitionQualityRule,
    block,
    config: _TransitionConfig,
) -> list[Violation]:
    """Collect sentence-level conditional-consequence findings."""
    if not config.detect_if_without_then:
        return []
    findings = 0
    violations: list[Violation] = []
    for sentence in block.sentences:
        if findings >= config.max_if_without_then_findings:
            break
        if not _is_if_consequence_without_then(
            sentence.projection.text, config.conditional_markers
        ):
            continue
        findings += 1
        violations.append(
            Violation(
                rule_id=rule.rule_id,
                message="Conditional consequence is stated without an explicit 'then' marker.",
                span=sentence.span,
                severity=rule.settings.severity,
                layer=rule.metadata.layer,
                evidence=RuleEvidence(
                    features={
                        "issue": "if_consequence_without_then",
                        "sentence_id": sentence.id,
                    }
                ),
                confidence=0.74,
                rationale=(
                    "The heuristic detects sentence-initial if-clauses that open a "
                    "consequence segment without an explicit consequence cue."
                ),
                rewrite_tactics=(
                    "Insert 'then' after the condition boundary to mark the "
                    "if-consequence transition explicitly.",
                ),
            )
        )
    return violations


def _implicit_contrast_violations(
    rule: TransitionQualityRule,
    block,
    ctx,
    config: _TransitionConfig,
) -> list[Violation]:
    """Collect implicit-contrast findings inside and across adjacent sentences."""
    if not config.detect_implicit_contrast:
        return []
    findings = 0
    violations: list[Violation] = []
    for sentence in block.sentences:
        if findings >= config.max_implicit_contrast_findings:
            break
        if not _has_inline_clause_contrast_without_marker(
            sentence.projection.text,
            config.explicit_contrast_pattern,
            config.positive_contrast_terms,
            config.negative_contrast_terms,
        ):
            continue
        findings += 1
        violations.append(
            Violation(
                rule_id=rule.rule_id,
                message=(
                    "The sentence implies a contrast but does not mark it with "
                    "an explicit contrast connector."
                ),
                span=sentence.span,
                severity=rule.settings.severity,
                layer=rule.metadata.layer,
                evidence=RuleEvidence(
                    features={
                        "issue": "implicit_contrast_without_marker",
                        "sentence_id": sentence.id,
                    }
                ),
                confidence=0.68,
                rationale=(
                    "The heuristic detects comma-joined clauses with opposed "
                    "polarity cues and no explicit contrast marker."
                ),
                rewrite_tactics=(
                    "Add an explicit contrast connector such as 'while' or "
                    "'whereas' to mark the contrast relation.",
                ),
            )
        )

    for index in range(1, len(block.sentences)):
        if findings >= config.max_implicit_contrast_findings:
            break
        previous = block.sentences[index - 1]
        current = block.sentences[index]
        overlap = ctx.features.sentence_overlap(previous.id, current.id)
        if overlap < config.min_overlap_for_implicit_contrast:
            continue
        if _starts_with_connector(current.projection.text, config.connector_pattern):
            continue
        if _starts_with_explicit_contrast(
            current.projection.text, config.explicit_contrast_pattern
        ):
            continue
        if not _has_polar_contrast(
            previous.projection.text,
            current.projection.text,
            config.positive_contrast_terms,
            config.negative_contrast_terms,
        ):
            continue
        findings += 1
        violations.append(
            Violation(
                rule_id=rule.rule_id,
                message=(
                    "Adjacent sentences imply a contrast but do not mark it "
                    "with an explicit contrast connector."
                ),
                span=current.span,
                severity=rule.settings.severity,
                layer=rule.metadata.layer,
                evidence=RuleEvidence(
                    features={
                        "issue": "implicit_contrast_without_marker",
                        "previous_sentence_id": previous.id,
                        "current_sentence_id": current.id,
                        "overlap": round(overlap, 3),
                    },
                    score=round(overlap, 3),
                    threshold=config.min_overlap_for_implicit_contrast,
                ),
                confidence=0.7,
                rationale=(
                    "The heuristic combines lexical continuity with opposed "
                    "polarity cues to detect implicit contrast relations."
                ),
                rewrite_tactics=(
                    "Add an explicit contrast connector such as 'while', "
                    "'whereas', or 'by contrast'.",
                ),
            )
        )
    return violations


def _unmarked_shift_violations(
    rule: TransitionQualityRule,
    block,
    ctx,
    config: _TransitionConfig,
) -> list[Violation]:
    """Collect unmarked transition-shift and connector-underuse findings."""
    if len(block.sentences) < 2:
        return []
    connector_count = 0
    overlaps: list[float] = []
    shift_findings = 0
    violations: list[Violation] = []
    for index in range(1, len(block.sentences)):
        previous = block.sentences[index - 1]
        current = block.sentences[index]
        current_text = current.projection.text
        if _starts_with_connector(current_text, config.connector_pattern):
            connector_count += 1
            continue
        overlap = ctx.features.sentence_overlap(previous.id, current.id)
        overlaps.append(overlap)
        if overlap >= config.min_overlap or _starts_with_linking_reference(
            current_text, config.reference_pattern
        ):
            continue
        if shift_findings >= config.max_shift_findings:
            continue
        shift_findings += 1
        violations.append(
            Violation(
                rule_id=rule.rule_id,
                message=(
                    "Adjacent sentences shift discourse without an explicit transition "
                    "or reference anchor."
                ),
                span=current.span,
                severity=rule.settings.severity,
                layer=rule.metadata.layer,
                evidence=RuleEvidence(
                    features={
                        "issue": "unmarked_shift",
                        "overlap": round(overlap, 3),
                        "previous_sentence_id": previous.id,
                        "current_sentence_id": current.id,
                    },
                    score=round(overlap, 3),
                    threshold=config.min_overlap,
                ),
                confidence=max(0.55, min(0.86, 0.9 - overlap)),
                rationale=(
                    "Transition articulation checks adjacent-sentence continuity with "
                    "bounded overlap and explicit opener signals."
                ),
                rewrite_tactics=(
                    "Add a connector or a concrete reference link that states how this "
                    "sentence follows from the previous one.",
                ),
            )
        )

    if len(block.sentences) < config.min_paragraph_sentences:
        return violations
    if connector_count > 0:
        return violations
    if not overlaps:
        return violations
    average_overlap = sum(overlaps) / len(overlaps)
    if average_overlap >= config.min_average_overlap:
        return violations
    violations.append(
        Violation(
            rule_id=rule.rule_id,
            message=(
                "The paragraph chains multiple sentences without explicit transition "
                "markers while local continuity remains weak."
            ),
            span=block.span,
            severity=rule.settings.severity,
            layer=rule.metadata.layer,
            evidence=RuleEvidence(
                features={
                    "issue": "connector_underuse",
                    "connector_count": connector_count,
                    "sentence_count": len(block.sentences),
                    "average_overlap": round(average_overlap, 3),
                },
                score=round(average_overlap, 3),
                threshold=config.min_average_overlap,
            ),
            confidence=0.62,
            rationale=(
                "Paragraph-level articulation checks require explicit connective framing "
                "when consecutive sentence overlap stays low."
            ),
            rewrite_tactics=(
                "Introduce transition markers at key sentence boundaries to make the "
                "argument steps explicit.",
            ),
        )
    )
    return violations


def _starts_with_connector(text: str, connector_pattern) -> bool:
    """Starts with connector."""
    return connector_pattern.search(text) is not None


def _starts_with_linking_reference(text: str, reference_pattern) -> bool:
    """Starts with linking reference."""
    return reference_pattern.search(text) is not None


def _block_in_structured_context(block) -> bool:
    """Return whether a paragraph block sits in a structured container context."""
    for sentence in block.sentences:
        if sentence.annotation_flags & {
            "list_item_context",
            "blockquote_context",
            "table_cell_context",
            "heading_context",
        }:
            return True
    return False


def _is_if_consequence_without_then(text: str, consequence_markers: frozenset[str]) -> bool:
    """Is if consequence without then."""
    if not text.strip():
        return False
    if "?" in text:
        return False
    if text.strip().endswith("?"):
        return False
    match = INITIAL_IF_BOUNDARY_RE.match(text)
    if match is None:
        return False
    condition = match.group("condition").strip().lower()
    if condition.startswith("and only if"):
        return False
    consequence = match.group("rest").strip().lower()
    if not consequence:
        return False
    if "?" in consequence:
        return False
    word_match = WORD_RE.search(consequence)
    if word_match is None:
        return False
    if word_match.group(0) in {"why", "how", "what", "which", "who", "where", "when"}:
        return False
    return word_match.group(0) not in consequence_markers


def _starts_with_explicit_contrast(text: str, explicit_contrast_pattern) -> bool:
    """Starts with explicit contrast."""
    return explicit_contrast_pattern.search(text) is not None


def _has_polar_contrast(
    previous_text: str,
    current_text: str,
    positive_terms: frozenset[str],
    negative_terms: frozenset[str],
) -> bool:
    """Has polar contrast."""
    previous_tokens = _token_set(previous_text)
    current_tokens = _token_set(current_text)
    previous_positive = bool(previous_tokens & positive_terms)
    previous_negative = bool(previous_tokens & negative_terms)
    current_positive = bool(current_tokens & positive_terms)
    current_negative = bool(current_tokens & negative_terms)
    return (previous_positive and current_negative) or (previous_negative and current_positive)


def _has_inline_clause_contrast_without_marker(
    text: str,
    explicit_contrast_pattern,
    positive_terms: frozenset[str],
    negative_terms: frozenset[str],
) -> bool:
    """Has inline clause contrast without marker."""
    if ";" in text:
        return False
    if "," not in text:
        return False
    if _starts_with_explicit_contrast(text, explicit_contrast_pattern):
        return False
    clauses = [clause.strip() for clause in text.split(",") if clause.strip()]
    if len(clauses) < 2:
        return False
    for index in range(1, len(clauses)):
        left = clauses[index - 1]
        right = clauses[index]
        if _starts_with_explicit_contrast(right, explicit_contrast_pattern):
            continue
        if _has_polar_contrast(left, right, positive_terms, negative_terms):
            return True
    return False


def _token_set(text: str) -> set[str]:
    """Token set."""
    return {token.group(0).lower() for token in WORD_RE.finditer(text)}


def register(registry) -> None:
    """Register.

    Parameters
    ----------
    registry : object
        Rule registry used to resolve implementations.
    """
    registry.add(TransitionQualityRule)
