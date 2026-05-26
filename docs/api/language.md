<a id="language"></a>

# Language

Language-pack abstractions and the English implementation.

<a id="module-hermeneia.language.base"></a>

<a id="base"></a>

## Base

Language-pack contracts and shared settings.

<a id="hermeneia.language.base.PreprocessingPolicy"></a>

### *class* hermeneia.language.base.PreprocessingPolicy(heavy_math_masking_ratio=0.4, symbol_dense_threshold=4, fragment_token_threshold=4, code_dominant_ratio=0.5)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Preprocessingpolicy.

<a id="hermeneia.language.base.PreprocessingPolicy.heavy_math_masking_ratio"></a>

#### heavy_math_masking_ratio *: [float](https://docs.python.org/3/library/functions.html#float)* *= 0.4*

<a id="hermeneia.language.base.PreprocessingPolicy.symbol_dense_threshold"></a>

#### symbol_dense_threshold *: [int](https://docs.python.org/3/library/functions.html#int)* *= 4*

<a id="hermeneia.language.base.PreprocessingPolicy.fragment_token_threshold"></a>

#### fragment_token_threshold *: [int](https://docs.python.org/3/library/functions.html#int)* *= 4*

<a id="hermeneia.language.base.PreprocessingPolicy.code_dominant_ratio"></a>

#### code_dominant_ratio *: [float](https://docs.python.org/3/library/functions.html#float)* *= 0.5*

<a id="hermeneia.language.base.LanguageLexicons"></a>

### *class* hermeneia.language.base.LanguageLexicons(weak_support_verbs=frozenset({}), nominalization_suffixes=(), nominalization_allowlist=frozenset({}), personal_pronoun_markers=(), generic_one_markers=(), bare_pronoun_openers=(), bare_pronoun_predicate_starters=(), strong_claim_markers=(), negative_markers=(), imperative_opening_verbs=(), indefinite_reference_terms=(), contractions=(), vague_mechanism_phrases=(), assumption_markers=(), proof_context_formal_openers=(), motivation_action_verbs=(), semicolon_parallel_starters=(), subordinate_clause_markers=(), display_interpretive_nouns=(), ambiguous_reference_verbs=(), ambiguous_reference_positions=(), explicit_reference_targets=(), citation_agent_verbs=(), citation_object_verbs=(), citation_forbidden_prepositions=(), citation_context_nouns=(), structural_metalanguage_terms=(), structural_metalanguage_positions=(), generic_link_reference_labels=(), procedural_link_terms=(), prose_math_phrases=(), assumption_hypothesis_terms=(), nominalization_linking_prepositions=frozenset({}), prepositions=frozenset({}), jargon_terms=frozenset({}), weak_final_words=frozenset({}), contrast_markers=(), explicit_contrast_markers=(), contrast_polarity_positive_terms=(), contrast_polarity_negative_terms=(), transition_connectors=(), transition_reference_heads=(), conditional_consequence_markers=(), inline_case_condition_markers=(), inline_case_fallback_markers=(), topic_sentence_openers=(), vague_rhetorical_openers=(), banned_transitions=(), abstract_framing_phrases=(), procedural_nominalization_terms=(), procedural_argument_markers=(), concrete_subject_terms=(), concrete_subject_action_verbs=(), abstract_compound_suffixes=(), lexicalized_compound_adjectives=(), verbose_preamble_markers=(), redundant_leadin_markers=(), list_framing_markers=(), concept_reference_labels=(), reformulation_markers=(), taxonomy_cardinality_targets=(), cardinality_number_words=(), filler_noun_terms=(), acronym_allowlist=frozenset({}), acronym_definition_stopwords=frozenset({}), definitional_markers=(), assumption_purpose_markers=(), formula_interpretation_markers=(), semicolon_connectors=(), qualitative_claim_markers=(), assumption_hypothesis_ignored_modifiers=frozenset({}), opening_purpose_markers=(), boilerplate_openers=(), imprecise_quantifier_terms=(), purpose_heading_markers=(), installation_heading_markers=(), usage_heading_markers=(), configuration_heading_markers=(), advanced_heading_markers=())

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Languagelexicons.

<a id="hermeneia.language.base.LanguageLexicons.weak_support_verbs"></a>

#### weak_support_verbs *: [frozenset](https://docs.python.org/3/library/stdtypes.html#frozenset)[[str](https://docs.python.org/3/library/stdtypes.html#str)]* *= frozenset({})*

<a id="hermeneia.language.base.LanguageLexicons.nominalization_suffixes"></a>

#### nominalization_suffixes *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguageLexicons.nominalization_allowlist"></a>

#### nominalization_allowlist *: [frozenset](https://docs.python.org/3/library/stdtypes.html#frozenset)[[str](https://docs.python.org/3/library/stdtypes.html#str)]* *= frozenset({})*

<a id="hermeneia.language.base.LanguageLexicons.personal_pronoun_markers"></a>

#### personal_pronoun_markers *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguageLexicons.generic_one_markers"></a>

#### generic_one_markers *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguageLexicons.bare_pronoun_openers"></a>

#### bare_pronoun_openers *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguageLexicons.bare_pronoun_predicate_starters"></a>

#### bare_pronoun_predicate_starters *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguageLexicons.strong_claim_markers"></a>

#### strong_claim_markers *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguageLexicons.negative_markers"></a>

#### negative_markers *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguageLexicons.imperative_opening_verbs"></a>

#### imperative_opening_verbs *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguageLexicons.indefinite_reference_terms"></a>

#### indefinite_reference_terms *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguageLexicons.contractions"></a>

#### contractions *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguageLexicons.vague_mechanism_phrases"></a>

#### vague_mechanism_phrases *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguageLexicons.assumption_markers"></a>

#### assumption_markers *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguageLexicons.proof_context_formal_openers"></a>

#### proof_context_formal_openers *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguageLexicons.motivation_action_verbs"></a>

#### motivation_action_verbs *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguageLexicons.semicolon_parallel_starters"></a>

#### semicolon_parallel_starters *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguageLexicons.subordinate_clause_markers"></a>

#### subordinate_clause_markers *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguageLexicons.display_interpretive_nouns"></a>

#### display_interpretive_nouns *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguageLexicons.ambiguous_reference_verbs"></a>

#### ambiguous_reference_verbs *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguageLexicons.ambiguous_reference_positions"></a>

#### ambiguous_reference_positions *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguageLexicons.explicit_reference_targets"></a>

#### explicit_reference_targets *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguageLexicons.citation_agent_verbs"></a>

#### citation_agent_verbs *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguageLexicons.citation_object_verbs"></a>

#### citation_object_verbs *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguageLexicons.citation_forbidden_prepositions"></a>

#### citation_forbidden_prepositions *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguageLexicons.citation_context_nouns"></a>

#### citation_context_nouns *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguageLexicons.structural_metalanguage_terms"></a>

#### structural_metalanguage_terms *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguageLexicons.structural_metalanguage_positions"></a>

#### structural_metalanguage_positions *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguageLexicons.generic_link_reference_labels"></a>

#### generic_link_reference_labels *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguageLexicons.procedural_link_terms"></a>

#### procedural_link_terms *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguageLexicons.prose_math_phrases"></a>

#### prose_math_phrases *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguageLexicons.assumption_hypothesis_terms"></a>

#### assumption_hypothesis_terms *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguageLexicons.nominalization_linking_prepositions"></a>

#### nominalization_linking_prepositions *: [frozenset](https://docs.python.org/3/library/stdtypes.html#frozenset)[[str](https://docs.python.org/3/library/stdtypes.html#str)]* *= frozenset({})*

<a id="hermeneia.language.base.LanguageLexicons.prepositions"></a>

#### prepositions *: [frozenset](https://docs.python.org/3/library/stdtypes.html#frozenset)[[str](https://docs.python.org/3/library/stdtypes.html#str)]* *= frozenset({})*

<a id="hermeneia.language.base.LanguageLexicons.jargon_terms"></a>

#### jargon_terms *: [frozenset](https://docs.python.org/3/library/stdtypes.html#frozenset)[[str](https://docs.python.org/3/library/stdtypes.html#str)]* *= frozenset({})*

<a id="hermeneia.language.base.LanguageLexicons.weak_final_words"></a>

#### weak_final_words *: [frozenset](https://docs.python.org/3/library/stdtypes.html#frozenset)[[str](https://docs.python.org/3/library/stdtypes.html#str)]* *= frozenset({})*

<a id="hermeneia.language.base.LanguageLexicons.contrast_markers"></a>

#### contrast_markers *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguageLexicons.explicit_contrast_markers"></a>

#### explicit_contrast_markers *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguageLexicons.contrast_polarity_positive_terms"></a>

#### contrast_polarity_positive_terms *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguageLexicons.contrast_polarity_negative_terms"></a>

#### contrast_polarity_negative_terms *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguageLexicons.transition_connectors"></a>

#### transition_connectors *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguageLexicons.transition_reference_heads"></a>

#### transition_reference_heads *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguageLexicons.conditional_consequence_markers"></a>

#### conditional_consequence_markers *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguageLexicons.inline_case_condition_markers"></a>

#### inline_case_condition_markers *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguageLexicons.inline_case_fallback_markers"></a>

#### inline_case_fallback_markers *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguageLexicons.topic_sentence_openers"></a>

#### topic_sentence_openers *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguageLexicons.vague_rhetorical_openers"></a>

#### vague_rhetorical_openers *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguageLexicons.banned_transitions"></a>

#### banned_transitions *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguageLexicons.abstract_framing_phrases"></a>

#### abstract_framing_phrases *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguageLexicons.procedural_nominalization_terms"></a>

#### procedural_nominalization_terms *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguageLexicons.procedural_argument_markers"></a>

#### procedural_argument_markers *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguageLexicons.concrete_subject_terms"></a>

#### concrete_subject_terms *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguageLexicons.concrete_subject_action_verbs"></a>

#### concrete_subject_action_verbs *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguageLexicons.abstract_compound_suffixes"></a>

#### abstract_compound_suffixes *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguageLexicons.lexicalized_compound_adjectives"></a>

#### lexicalized_compound_adjectives *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguageLexicons.verbose_preamble_markers"></a>

#### verbose_preamble_markers *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguageLexicons.redundant_leadin_markers"></a>

#### redundant_leadin_markers *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguageLexicons.list_framing_markers"></a>

#### list_framing_markers *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguageLexicons.concept_reference_labels"></a>

#### concept_reference_labels *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguageLexicons.reformulation_markers"></a>

#### reformulation_markers *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguageLexicons.taxonomy_cardinality_targets"></a>

#### taxonomy_cardinality_targets *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguageLexicons.cardinality_number_words"></a>

#### cardinality_number_words *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguageLexicons.filler_noun_terms"></a>

#### filler_noun_terms *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguageLexicons.acronym_allowlist"></a>

#### acronym_allowlist *: [frozenset](https://docs.python.org/3/library/stdtypes.html#frozenset)[[str](https://docs.python.org/3/library/stdtypes.html#str)]* *= frozenset({})*

<a id="hermeneia.language.base.LanguageLexicons.acronym_definition_stopwords"></a>

#### acronym_definition_stopwords *: [frozenset](https://docs.python.org/3/library/stdtypes.html#frozenset)[[str](https://docs.python.org/3/library/stdtypes.html#str)]* *= frozenset({})*

<a id="hermeneia.language.base.LanguageLexicons.definitional_markers"></a>

#### definitional_markers *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguageLexicons.assumption_purpose_markers"></a>

#### assumption_purpose_markers *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguageLexicons.formula_interpretation_markers"></a>

#### formula_interpretation_markers *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguageLexicons.semicolon_connectors"></a>

#### semicolon_connectors *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguageLexicons.qualitative_claim_markers"></a>

#### qualitative_claim_markers *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguageLexicons.assumption_hypothesis_ignored_modifiers"></a>

#### assumption_hypothesis_ignored_modifiers *: [frozenset](https://docs.python.org/3/library/stdtypes.html#frozenset)[[str](https://docs.python.org/3/library/stdtypes.html#str)]* *= frozenset({})*

<a id="hermeneia.language.base.LanguageLexicons.opening_purpose_markers"></a>

#### opening_purpose_markers *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguageLexicons.boilerplate_openers"></a>

#### boilerplate_openers *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguageLexicons.imprecise_quantifier_terms"></a>

#### imprecise_quantifier_terms *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguageLexicons.purpose_heading_markers"></a>

#### purpose_heading_markers *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguageLexicons.installation_heading_markers"></a>

#### installation_heading_markers *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguageLexicons.usage_heading_markers"></a>

#### usage_heading_markers *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguageLexicons.configuration_heading_markers"></a>

#### configuration_heading_markers *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguageLexicons.advanced_heading_markers"></a>

#### advanced_heading_markers *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.language.base.LanguagePack"></a>

### *class* hermeneia.language.base.LanguagePack(code, name, parser_model, preprocessing, lexicons, rule_defaults=<factory>, supported_rules=frozenset({}))

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Languagepack.

<a id="hermeneia.language.base.LanguagePack.code"></a>

#### code *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

<a id="hermeneia.language.base.LanguagePack.name"></a>

#### name *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

<a id="hermeneia.language.base.LanguagePack.parser_model"></a>

#### parser_model *: [str](https://docs.python.org/3/library/stdtypes.html#str) | [None](https://docs.python.org/3/library/constants.html#None)*

<a id="hermeneia.language.base.LanguagePack.preprocessing"></a>

#### preprocessing *: [PreprocessingPolicy](#hermeneia.language.base.PreprocessingPolicy)*

<a id="hermeneia.language.base.LanguagePack.lexicons"></a>

#### lexicons *: [LanguageLexicons](#hermeneia.language.base.LanguageLexicons)*

<a id="hermeneia.language.base.LanguagePack.rule_defaults"></a>

#### rule_defaults *: [Mapping](https://docs.python.org/3/library/typing.html#typing.Mapping)[[str](https://docs.python.org/3/library/stdtypes.html#str), [Mapping](https://docs.python.org/3/library/typing.html#typing.Mapping)[[str](https://docs.python.org/3/library/stdtypes.html#str), [object](https://docs.python.org/3/library/functions.html#object)]]*

<a id="hermeneia.language.base.LanguagePack.supported_rules"></a>

#### supported_rules *: [frozenset](https://docs.python.org/3/library/stdtypes.html#frozenset)[[str](https://docs.python.org/3/library/stdtypes.html#str)]* *= frozenset({})*

<a id="module-hermeneia.language.en"></a>

<a id="english-pack"></a>

## English pack

Built-in English language pack.

<a id="module-hermeneia.language.registry"></a>

<a id="registry"></a>

## Registry

Built-in language-pack registry.

<a id="hermeneia.language.registry.LanguageRegistry"></a>

### *class* hermeneia.language.registry.LanguageRegistry

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Languageregistry.

<a id="hermeneia.language.registry.LanguageRegistry.__init__"></a>

#### \_\_init_\_()

Initialize the instance.

<a id="hermeneia.language.registry.LanguageRegistry.get"></a>

#### get(code)

Get.

* **Parameters:**
  **code** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Input value for `code`.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [LanguagePack](#hermeneia.language.base.LanguagePack)

<a id="hermeneia.language.registry.LanguageRegistry.register"></a>

#### register(pack)

Register.

* **Parameters:**
  **pack** ([*LanguagePack*](#hermeneia.language.base.LanguagePack)) – Input value for `pack`.

<a id="hermeneia.language.registry.LanguageRegistry.supported_codes"></a>

#### supported_codes()

Supported codes.

* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), …]
