from __future__ import annotations

import pytest

from hermeneia.rules.base import RuleKind, Severity


@pytest.mark.parametrize(
    "rule_id",
    [
        "surface.nominalization",
        "surface.abstract_framing",
        "surface.banned_transition",
        "surface.generic_link_text",
        "surface.abstract_compound_modifier",
        "surface.case_scaffolding",
        "math.display_math",
        "surface.bare_pronoun_opening",
    ],
)
def test_hard_rule_policy_defaults_to_error_blockers(registry, rule_id: str) -> None:
    metadata = registry.get(rule_id).metadata
    assert metadata.kind == RuleKind.HARD_CONSTRAINT
    assert metadata.default_severity == Severity.ERROR
