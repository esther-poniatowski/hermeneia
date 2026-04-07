"""Built-in English language pack."""

from __future__ import annotations

from hermeneia.language.base import LanguageLexicons, LanguagePack, PreprocessingPolicy

ENGLISH_PACK = LanguagePack(
    code="en",
    name="English",
    parser_model="en_core_web_sm",
    preprocessing=PreprocessingPolicy(),
    lexicons=LanguageLexicons(
        weak_support_verbs=frozenset(
            {"be", "is", "are", "was", "were", "have", "has", "do", "does", "did"}
        ),
        nominalization_suffixes=("tion", "sion", "ment", "ance", "ence", "ity"),
        strong_claim_markers=(
            "proves",
            "demonstrates",
            "shows",
            "establishes",
            "guarantees",
            "always",
            "never",
            "clearly",
            "obviously",
        ),
        contrast_markers=(
            "however",
            "in contrast",
            "conversely",
            "whereas",
            "by contrast",
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
            "it is easy to see",
            "it follows that",
        ),
        acronym_allowlist=frozenset({"API", "CLI", "NLP"}),
        definitional_markers=(
            "is defined as",
            "denote",
            "means",
            "refers to",
            "call this",
        ),
    ),
    rule_defaults={
        "surface.sentence_length": {"options": {"max_words": 28}},
        "discourse.subject_verb_distance": {"options": {"max_distance": 8}},
        "audience.claim_calibration": {"options": {"lookback_sentences": 3}},
        "paragraph.topic_sentence": {"options": {"minimum_score": 0.45}},
    },
)
