"""Language-pack contracts and shared settings."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping


@dataclass(frozen=True)
class PreprocessingPolicy:
    heavy_math_masking_ratio: float = 0.4
    symbol_dense_threshold: int = 4
    fragment_token_threshold: int = 4
    code_dominant_ratio: float = 0.5


@dataclass(frozen=True)
class LanguageLexicons:
    weak_support_verbs: frozenset[str] = frozenset()
    nominalization_suffixes: tuple[str, ...] = ()
    strong_claim_markers: tuple[str, ...] = ()
    pronoun_scaffolding_markers: tuple[str, ...] = ()
    imperative_opening_verbs: tuple[str, ...] = ()
    indefinite_reference_terms: tuple[str, ...] = ()
    contractions: tuple[str, ...] = ()
    vague_mechanism_phrases: tuple[str, ...] = ()
    assumption_markers: tuple[str, ...] = ()
    proof_context_formal_openers: tuple[str, ...] = ()
    motivation_action_verbs: tuple[str, ...] = ()
    semicolon_parallel_starters: tuple[str, ...] = ()
    subordinate_clause_markers: tuple[str, ...] = ()
    display_interpretive_nouns: tuple[str, ...] = ()
    ambiguous_reference_verbs: tuple[str, ...] = ()
    ambiguous_reference_positions: tuple[str, ...] = ()
    explicit_reference_targets: tuple[str, ...] = ()
    generic_link_reference_labels: tuple[str, ...] = ()
    prose_math_phrases: tuple[str, ...] = ()
    assumption_hypothesis_terms: tuple[str, ...] = ()
    nominalization_linking_prepositions: frozenset[str] = frozenset()
    prepositions: frozenset[str] = frozenset()
    jargon_terms: frozenset[str] = frozenset()
    weak_final_words: frozenset[str] = frozenset()
    contrast_markers: tuple[str, ...] = ()
    transition_connectors: tuple[str, ...] = ()
    transition_reference_heads: tuple[str, ...] = ()
    topic_sentence_openers: tuple[str, ...] = ()
    vague_rhetorical_openers: tuple[str, ...] = ()
    banned_transitions: tuple[str, ...] = ()
    abstract_framing_phrases: tuple[str, ...] = ()
    abstract_compound_suffixes: tuple[str, ...] = ()
    concept_reference_labels: tuple[str, ...] = ()
    reformulation_markers: tuple[str, ...] = ()
    acronym_allowlist: frozenset[str] = frozenset()
    acronym_definition_stopwords: frozenset[str] = frozenset()
    definitional_markers: tuple[str, ...] = ()
    assumption_purpose_markers: tuple[str, ...] = ()
    formula_interpretation_markers: tuple[str, ...] = ()
    semicolon_connectors: tuple[str, ...] = ()
    qualitative_claim_markers: tuple[str, ...] = ()
    assumption_hypothesis_ignored_modifiers: frozenset[str] = frozenset()


@dataclass(frozen=True)
class LanguagePack:
    code: str
    name: str
    parser_model: str | None
    preprocessing: PreprocessingPolicy
    lexicons: LanguageLexicons
    rule_defaults: Mapping[str, Mapping[str, object]] = field(default_factory=dict)
    supported_rules: frozenset[str] = frozenset()
