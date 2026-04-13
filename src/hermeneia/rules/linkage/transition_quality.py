"""Discourse-transition articulation heuristics."""

from __future__ import annotations

import re

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
        min_overlap = self.settings.float_option("min_overlap_without_connector", 0.18)
        max_shift_findings = self.settings.int_option("max_shift_findings", 3)
        min_paragraph_sentences = self.settings.int_option("min_paragraph_sentences", 4)
        min_average_overlap = self.settings.float_option(
            "min_average_overlap_without_connectors", 0.35
        )
        detect_if_without_then = self.settings.bool_option(
            "detect_if_without_then", True
        )
        max_if_without_then_findings = self.settings.int_option(
            "max_if_without_then_findings", 3
        )
        detect_implicit_contrast = self.settings.bool_option(
            "detect_implicit_contrast", True
        )
        max_implicit_contrast_findings = self.settings.int_option(
            "max_implicit_contrast_findings", 3
        )
        min_overlap_for_implicit_contrast = self.settings.float_option(
            "min_overlap_for_implicit_contrast", 0.2
        )
        connector_pattern = compile_leading_phrase_regex(
            tuple(ctx.language_pack.lexicons.transition_connectors)
        )
        explicit_contrast_pattern = compile_inline_phrase_regex(
            tuple(ctx.language_pack.lexicons.explicit_contrast_markers)
        )
        reference_pattern = compile_prefixed_term_regex(
            ("this", "these", "that", "such"),
            tuple(ctx.language_pack.lexicons.transition_reference_heads),
            anchored=True,
        )
        conditional_markers = frozenset(
            marker.lower()
            for marker in ctx.language_pack.lexicons.conditional_consequence_markers
        )
        positive_contrast_terms = frozenset(
            term.lower()
            for term in ctx.language_pack.lexicons.contrast_polarity_positive_terms
        )
        negative_contrast_terms = frozenset(
            term.lower()
            for term in ctx.language_pack.lexicons.contrast_polarity_negative_terms
        )
        violations: list[Violation] = []
        for block in iter_blocks(
            doc, {BlockKind.PARAGRAPH, BlockKind.BLOCK_QUOTE, BlockKind.LIST_ITEM}
        ):
            if detect_if_without_then:
                if_without_then_findings = 0
                for sentence in block.sentences:
                    if if_without_then_findings >= max_if_without_then_findings:
                        break
                    if not _is_if_consequence_without_then(
                        sentence.projection.text, conditional_markers
                    ):
                        continue
                    if_without_then_findings += 1
                    violations.append(
                        Violation(
                            rule_id=self.rule_id,
                            message=(
                                "Conditional consequence is stated without an explicit "
                                "'then' marker."
                            ),
                            span=sentence.span,
                            severity=self.settings.severity,
                            layer=self.metadata.layer,
                            evidence=RuleEvidence(
                                features={
                                    "issue": "if_consequence_without_then",
                                    "sentence_id": sentence.id,
                                }
                            ),
                            confidence=0.74,
                            rationale=(
                                "The heuristic detects sentence-initial if-clauses that "
                                "open a consequence segment without an explicit consequence cue."
                            ),
                            rewrite_tactics=(
                                "Insert 'then' after the condition boundary to mark the "
                                "if-consequence transition explicitly.",
                            ),
                        )
                    )

            implicit_contrast_findings = 0
            if detect_implicit_contrast:
                for sentence in block.sentences:
                    if implicit_contrast_findings >= max_implicit_contrast_findings:
                        break
                    if not _has_inline_clause_contrast_without_marker(
                        sentence.projection.text,
                        explicit_contrast_pattern,
                        positive_contrast_terms,
                        negative_contrast_terms,
                    ):
                        continue
                    implicit_contrast_findings += 1
                    violations.append(
                        Violation(
                            rule_id=self.rule_id,
                            message=(
                                "The sentence implies a contrast but does not mark it with "
                                "an explicit contrast connector."
                            ),
                            span=sentence.span,
                            severity=self.settings.severity,
                            layer=self.metadata.layer,
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
                    if implicit_contrast_findings >= max_implicit_contrast_findings:
                        break
                    previous = block.sentences[index - 1]
                    current = block.sentences[index]
                    overlap = ctx.features.sentence_overlap(previous.id, current.id)
                    if overlap < min_overlap_for_implicit_contrast:
                        continue
                    if _starts_with_connector(
                        current.projection.text, connector_pattern
                    ):
                        continue
                    if _starts_with_explicit_contrast(
                        current.projection.text, explicit_contrast_pattern
                    ):
                        continue
                    if not _has_polar_contrast(
                        previous.projection.text,
                        current.projection.text,
                        positive_contrast_terms,
                        negative_contrast_terms,
                    ):
                        continue
                    implicit_contrast_findings += 1
                    violations.append(
                        Violation(
                            rule_id=self.rule_id,
                            message=(
                                "Adjacent sentences imply a contrast but do not mark it "
                                "with an explicit contrast connector."
                            ),
                            span=current.span,
                            severity=self.settings.severity,
                            layer=self.metadata.layer,
                            evidence=RuleEvidence(
                                features={
                                    "issue": "implicit_contrast_without_marker",
                                    "previous_sentence_id": previous.id,
                                    "current_sentence_id": current.id,
                                    "overlap": round(overlap, 3),
                                },
                                score=round(overlap, 3),
                                threshold=min_overlap_for_implicit_contrast,
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

            if len(block.sentences) < 2:
                continue
            connector_count = 0
            overlaps: list[float] = []
            shift_findings = 0
            for index in range(1, len(block.sentences)):
                previous = block.sentences[index - 1]
                current = block.sentences[index]
                current_text = current.projection.text
                if _starts_with_connector(current_text, connector_pattern):
                    connector_count += 1
                    continue
                overlap = ctx.features.sentence_overlap(previous.id, current.id)
                overlaps.append(overlap)
                if overlap >= min_overlap or _starts_with_linking_reference(
                    current_text, reference_pattern
                ):
                    continue
                if shift_findings >= max_shift_findings:
                    continue
                shift_findings += 1
                violations.append(
                    Violation(
                        rule_id=self.rule_id,
                        message=(
                            "Adjacent sentences shift discourse without an explicit transition "
                            "or reference anchor."
                        ),
                        span=current.span,
                        severity=self.settings.severity,
                        layer=self.metadata.layer,
                        evidence=RuleEvidence(
                            features={
                                "issue": "unmarked_shift",
                                "overlap": round(overlap, 3),
                                "previous_sentence_id": previous.id,
                                "current_sentence_id": current.id,
                            },
                            score=round(overlap, 3),
                            threshold=min_overlap,
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
            if len(block.sentences) < min_paragraph_sentences:
                continue
            if connector_count > 0:
                continue
            if not overlaps:
                continue
            average_overlap = sum(overlaps) / len(overlaps)
            if average_overlap >= min_average_overlap:
                continue
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    message=(
                        "The paragraph chains multiple sentences without explicit transition "
                        "markers while local continuity remains weak."
                    ),
                    span=block.span,
                    severity=self.settings.severity,
                    layer=self.metadata.layer,
                    evidence=RuleEvidence(
                        features={
                            "issue": "connector_underuse",
                            "connector_count": connector_count,
                            "sentence_count": len(block.sentences),
                            "average_overlap": round(average_overlap, 3),
                        },
                        score=round(average_overlap, 3),
                        threshold=min_average_overlap,
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


def _is_if_consequence_without_then(
    text: str, consequence_markers: frozenset[str]
) -> bool:
    """Is if consequence without then."""
    if not text.strip():
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
    return (previous_positive and current_negative) or (
        previous_negative and current_positive
    )


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
