from __future__ import annotations

import pytest

from hermeneia.rules.base import RuleKind, Severity


@pytest.mark.parametrize(
    "rule_id",
    [
        "vocabulary.nominalization",
        "vocabulary.abstract_framing",
        "linkage.banned_transition",
        "reference.generic_link_text",
        "vocabulary.abstract_compound_modifier",
        "linkage.case_scaffolding",
        "math.display_math",
        "reference.bare_pronoun_opening",
    ],
)
def test_hard_rule_policy_defaults_to_error_blockers(registry, rule_id: str) -> None:
    metadata = registry.get(rule_id).metadata
    assert metadata.kind == RuleKind.HARD_CONSTRAINT
    assert metadata.default_severity == Severity.ERROR
