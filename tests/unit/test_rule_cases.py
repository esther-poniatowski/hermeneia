"""Planted cases of the rules, read from ``tests/fixtures/rule_cases.yaml``.

Each source listed under ``fires`` must yield at least one finding of its rule, and each source
listed under ``passes`` none, so that a missed construction and a false positive both fail. A new
case is a new line of the fixture, and needs no code.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from hermeneia.document.annotator import SpaCyDocumentAnnotator
from hermeneia.document.indexes import FeatureStore
from hermeneia.document.markdown import MarkdownDocumentParser
from hermeneia.document.parser import ParseRequest
from hermeneia.rules.base import RuleContext

CASES = Path(__file__).resolve().parents[1] / "fixtures" / "rule_cases.yaml"


def _cases() -> list[tuple[str, str, bool]]:
    """Return every planted case as (rule id, source, whether the rule must fire)."""
    data = yaml.safe_load(CASES.read_text(encoding="utf-8"))
    return [
        (rule_id, source, expected == "fires")
        for rule_id, groups in data.items()
        for expected in ("fires", "passes")
        for source in groups.get(expected, [])
    ]


CASE_LIST = _cases()


@pytest.mark.parametrize(
    ("rule_id", "source", "fires"),
    CASE_LIST,
    ids=[
        f"{rule_id}:{'fires' if fires else 'passes'}:{index}"
        for index, (rule_id, _, fires) in enumerate(CASE_LIST)
    ],
)
def test_rule_case(
    rule_id: str, source: str, fires: bool, registry, language_pack, research_profile
) -> None:
    text = source if source.endswith("\n") else source + "\n"
    document = MarkdownDocumentParser(language_pack).parse(
        ParseRequest(source=text, path=Path("case.md"))
    )
    document = (
        SpaCyDocumentAnnotator(language_pack.parser_model)
        .annotate(document, research_profile)
        .document
    )
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules[rule_id])
    found = [violation.message for violation in rule.check(document, context)]
    assert bool(found) == fires, found


def test_every_case_names_a_registered_rule(registry, research_profile) -> None:
    assert {rule_id for rule_id, _, _ in CASE_LIST} <= set(research_profile.rules)
