"""Built-in English language pack."""

from __future__ import annotations

from hermeneia.language.base import LanguageLexicons, LanguagePack, PreprocessingPolicy

ENGLISH_SPACY_MODEL = "en_core_web_sm"
ENGLISH_SPACY_MODEL_VERSION = "3.8.0"

ENGLISH_PACK = LanguagePack(
    code="en",
    name="English",
    parser_model=ENGLISH_SPACY_MODEL,
    preprocessing=PreprocessingPolicy(),
    lexicons=LanguageLexicons(
        weak_support_verbs=frozenset(
            {"be", "is", "are", "was", "were", "have", "has", "do", "does", "did"}
        ),
        nominalization_suffixes=("tion", "sion", "ment", "ance", "ence", "ity"),
        strong_claim_markers=(
            "prove",
            "demonstrate",
            "show",
            "establish",
            "guarantee",
            "always",
            "never",
            "clearly",
            "obviously",
        ),
        weak_final_words=frozenset(
            {
                "is",
                "are",
                "was",
                "were",
                "be",
                "been",
                "being",
                "follow",
                "follows",
                "this",
                "that",
                "it",
                "there",
                "thing",
                "stuff",
                "result",
            }
        ),
        contrast_markers=(
            "however",
            "in contrast",
            "conversely",
            "whereas",
            "by contrast",
        ),
        transition_connectors=(
            "however",
            "therefore",
            "thus",
            "hence",
            "consequently",
            "accordingly",
            "in contrast",
            "conversely",
            "meanwhile",
            "by contrast",
            "instead",
            "nevertheless",
        ),
        transition_reference_heads=(
            "result",
            "claim",
            "step",
            "argument",
            "estimate",
            "bound",
            "construction",
            "observation",
            "property",
        ),
        topic_sentence_openers=(
            "however",
            "for example",
            "specifically",
            "in particular",
            "for instance",
        ),
        vague_rhetorical_openers=(
            "to see this",
            "it should be noted that",
            "it is worth noting that",
            "in this context",
            "in this regard",
            "as can be seen",
            "it can be observed that",
        ),
        banned_transitions=(
            "equivalently",
            "more explicitly",
            "this gives",
            "rewriting",
            "note that",
            "notice that",
            "recall that",
            "observe that",
            "clearly",
            "obviously",
            "naturally",
            "of course",
            "straightforward",
            "it can be shown",
            "it is easy to",
            "it can be verified",
            "it can be checked",
            "it can be seen",
            "it follows that",
        ),
        abstract_framing_phrases=(
            "the fact that",
            "the question of",
            "the issue of",
            "in terms of",
            "is given by",
        ),
        abstract_compound_suffixes=(
            "specific",
            "dependent",
            "based",
            "driven",
            "oriented",
            "related",
            "centric",
        ),
        concept_reference_labels=(
            "method",
            "approach",
            "framework",
            "strategy",
            "procedure",
            "technique",
            "model",
            "pipeline",
            "scheme",
            "mechanism",
            "argument",
            "proof",
        ),
        reformulation_markers=(
            "in other words",
            "that is",
            "i.e.",
            "equivalently",
            "put differently",
            "stated differently",
        ),
        acronym_allowlist=frozenset({"API", "CLI", "NLP"}),
        acronym_definition_stopwords=frozenset(
            {"a", "an", "and", "for", "in", "of", "on", "the", "to", "with", "by"}
        ),
        definitional_markers=(
            "defined as",
            "define",
            "denote",
            "denotes",
            "mean",
            "means",
            "refer to",
            "refers to",
            "called",
            "written as",
            "measured by",
        ),
        assumption_hypothesis_ignored_modifiers=frozenset(
            {"same", "above", "previous", "following", "main", "key", "central"}
        ),
    ),
    rule_defaults={
        "surface.sentence_length": {"options": {"max_words": 28}},
        "surface.prep_chain": {"options": {"max_prepositions": 4}},
        "surface.noun_cluster": {"options": {"max_cluster_tokens": 4}},
        "discourse.subject_verb_distance": {"options": {"max_distance": 8}},
        "discourse.subordinate_clause": {"options": {"max_subordinate_clauses": 2}},
        "discourse.transition_quality": {
            "options": {
                "min_overlap_without_connector": 0.18,
                "min_paragraph_sentences": 4,
                "min_average_overlap_without_connectors": 0.35,
            }
        },
        "audience.acronym_burden": {
            "options": {
                "min_acronym_mentions_for_overuse": 4,
                "max_acronym_to_full_form_ratio": 2.0,
            }
        },
        "audience.claim_calibration": {"options": {"lookback_sentences": 3}},
        "paragraph.sentence_redundancy": {"options": {"min_overlap": 0.78}},
        "paragraph.paragraph_redundancy": {
            "options": {"min_similarity": 0.88, "min_lexical_overlap": 0.35, "max_findings": 5}
        },
        "paragraph.topic_sentence": {"options": {"minimum_score": 0.45}},
        "structure.section_balance": {"options": {"max_ratio": 3.5}},
    },
)
