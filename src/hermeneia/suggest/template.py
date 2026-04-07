"""Guarded candidate rewrites."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class RewriteCandidate:
    tactic: str
    candidate_rewrite: str | None = None


CONTRACTION_EXPANSIONS: Mapping[str, str] = {
    "it's": "it is",
    "that's": "that is",
    "there's": "there is",
    "here's": "here is",
    "let's": "let us",
    "can't": "cannot",
    "won't": "will not",
    "don't": "do not",
    "doesn't": "does not",
    "didn't": "did not",
    "isn't": "is not",
    "aren't": "are not",
    "wasn't": "was not",
    "weren't": "were not",
    "haven't": "have not",
    "hasn't": "has not",
    "hadn't": "had not",
    "wouldn't": "would not",
    "shouldn't": "should not",
    "couldn't": "could not",
    "i'm": "I am",
    "i've": "I have",
    "i'll": "I will",
    "you're": "you are",
    "you've": "you have",
    "you'll": "you will",
    "we're": "we are",
    "we've": "we have",
    "we'll": "we will",
    "they're": "they are",
    "they've": "they have",
    "they'll": "they will",
}

NOMINALIZATION_VERB_MAP: Mapping[str, str] = {
    "assumption": "assume",
    "definition": "define",
    "analysis": "analyze",
    "evaluation": "evaluate",
    "construction": "construct",
    "representation": "represent",
    "approximation": "approximate",
    "observation": "observe",
    "derivation": "derive",
}


def rewrite_for_contraction(contraction: str | None) -> RewriteCandidate:
    if contraction is None:
        return RewriteCandidate(tactic="Expand contractions in technical prose")
    normalized = contraction.lower()
    expansion = CONTRACTION_EXPANSIONS.get(normalized)
    if expansion is None:
        return RewriteCandidate(tactic="Expand contractions in technical prose")
    return RewriteCandidate(
        tactic=f"Expand '{contraction}' to its full form.",
        candidate_rewrite=expansion,
    )


def rewrite_for_proof_marker() -> RewriteCandidate:
    return RewriteCandidate(
        tactic="Introduce an explicit proof opener before the proof body.",
        candidate_rewrite="*Proof.*",
    )


def rewrite_for_nominalization(
    nominalization: str | None,
    support_verb: str | None,
) -> RewriteCandidate | None:
    if nominalization is None:
        return None
    verb = NOMINALIZATION_VERB_MAP.get(nominalization.lower())
    if verb is None:
        return None
    if support_verb:
        tactic = (
            f"Replace weak support phrase '{support_verb} {nominalization}' "
            f"with a direct verb form."
        )
    else:
        tactic = "Prefer a direct verb form over weak support-noun phrasing."
    return RewriteCandidate(tactic=tactic, candidate_rewrite=verb)


def rewrite_for_passive_voice(
    actor: str | None,
    participle: str | None,
) -> RewriteCandidate | None:
    if actor is None:
        return None
    cleaned_actor = actor.strip()
    if not cleaned_actor:
        return None
    capitalized_actor = cleaned_actor[0].upper() + cleaned_actor[1:]
    tactic = f"Rewrite in active voice with '{cleaned_actor}' as the grammatical subject."
    if participle and participle.lower().endswith("ed"):
        return RewriteCandidate(
            tactic=tactic,
            candidate_rewrite=f"{capitalized_actor} {participle} ...",
        )
    return RewriteCandidate(tactic=tactic)


def tactic_only(message: str) -> RewriteCandidate:
    return RewriteCandidate(tactic=message)


def no_deterministic_rewrite_available() -> RewriteCandidate:
    return RewriteCandidate(
        tactic="No deterministic rewrite candidate is available for this rule; revise manually using the reported evidence."
    )
