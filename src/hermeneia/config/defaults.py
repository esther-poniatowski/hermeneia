"""Built-in profile and runtime defaults."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ProfilePreset:
    name: str
    audience: str
    genre: str
    section: str
    register: str
    active_rules: tuple[str, ...]
    rule_overrides: dict[str, dict[str, object]] = field(default_factory=dict)


DEFAULT_PROFILE = "research"

PROFILE_PRESETS: dict[str, ProfilePreset] = {
    "research": ProfilePreset(
        name="research",
        audience="specialist",
        genre="research_note",
        section="body",
        register="formal",
        active_rules=(
            "surface.sentence_length",
            "surface.contraction",
            "surface.nominalization",
            "surface.banned_transition",
            "discourse.subject_verb_distance",
            "paragraph.topic_sentence",
            "structure.heading_parallelism",
            "audience.acronym_burden",
            "audience.definition_before_use",
            "audience.claim_calibration",
        ),
        rule_overrides={
            "surface.sentence_length": {"max_words": 32},
            "discourse.subject_verb_distance": {"max_distance": 10},
        },
    ),
    "pedagogical": ProfilePreset(
        name="pedagogical",
        audience="learner",
        genre="lecture_note",
        section="body",
        register="pedagogical",
        active_rules=(
            "surface.sentence_length",
            "surface.contraction",
            "surface.nominalization",
            "surface.banned_transition",
            "discourse.subject_verb_distance",
            "paragraph.topic_sentence",
            "structure.heading_parallelism",
            "audience.acronym_burden",
            "audience.definition_before_use",
            "audience.claim_calibration",
        ),
        rule_overrides={
            "surface.sentence_length": {"max_words": 24},
            "discourse.subject_verb_distance": {"max_distance": 6},
            "paragraph.topic_sentence": {"minimum_score": 0.55},
        },
    ),
    "math": ProfilePreset(
        name="math",
        audience="specialist",
        genre="mathematical_note",
        section="body",
        register="mathematical",
        active_rules=(
            "surface.sentence_length",
            "surface.nominalization",
            "surface.banned_transition",
            "math.display_math",
            "math.bare_symbol",
            "math.imperative_opening",
            "discourse.subject_verb_distance",
            "paragraph.topic_sentence",
            "audience.acronym_burden",
            "audience.definition_before_use",
            "audience.claim_calibration",
        ),
        rule_overrides={
            "surface.sentence_length": {"max_words": 26},
            "math.display_math": {"require_leadin": True},
            "audience.claim_calibration": {"lookback_sentences": 4},
        },
    ),
}
