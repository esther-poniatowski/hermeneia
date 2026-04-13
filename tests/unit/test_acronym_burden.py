from __future__ import annotations

from pathlib import Path

from hermeneia.config.profile import ProfileResolver
from hermeneia.config.schema import parse_project_config
from hermeneia.document.indexes import FeatureStore
from hermeneia.document.markdown import MarkdownDocumentParser
from hermeneia.document.parser import ParseRequest
from hermeneia.rules.base import RuleContext


def _parse(language_pack, source: str):
    return MarkdownDocumentParser(language_pack).parse(
        ParseRequest(source=source, path=Path("demo.md"))
    )


def test_acronym_burden_emits_for_undefined_acronym(
    registry, language_pack, research_profile
) -> None:
    source = "The PDE is solved numerically.\n"
    document = _parse(language_pack, source)
    context = RuleContext(
        research_profile, language_pack, FeatureStore(document, document.indexes)
    )
    rule = registry.instantiate(research_profile.rules["terminology.acronym_burden"])
    violations = rule.check(document, context)
    assert len(violations) == 1
    assert violations[0].rule_id == "terminology.acronym_burden"
    assert violations[0].evidence is not None
    assert violations[0].evidence.features["issue"] == "undefined_acronym"


def test_acronym_burden_skips_when_definition_precedes_use(
    registry, language_pack, research_profile
) -> None:
    source = (
        "Partial Differential Equation (PDE) governs the field evolution.\n"
        "The PDE is solved numerically.\n"
    )
    document = _parse(language_pack, source)
    context = RuleContext(
        research_profile, language_pack, FeatureStore(document, document.indexes)
    )
    rule = registry.instantiate(research_profile.rules["terminology.acronym_burden"])
    assert rule.check(document, context) == []


def test_acronym_burden_emits_for_acronym_overuse_against_full_form(
    registry, language_pack, research_profile
) -> None:
    source = (
        "Partial Differential Equation (PDE) model is stable.\n"
        "The PDE converges in the weak norm.\n"
        "The PDE is consistent with the boundary data.\n"
        "The PDE remains bounded under perturbation.\n"
        "The PDE is solved numerically.\n"
    )
    document = _parse(language_pack, source)
    context = RuleContext(
        research_profile, language_pack, FeatureStore(document, document.indexes)
    )
    rule = registry.instantiate(research_profile.rules["terminology.acronym_burden"])
    violations = rule.check(document, context)
    assert len(violations) == 1
    violation = violations[0]
    assert violation.rule_id == "terminology.acronym_burden"
    assert violation.evidence is not None
    assert violation.evidence.features["issue"] == "acronym_overuse"


def test_acronym_burden_ignores_callout_label_tokens(
    registry, language_pack, research_profile
) -> None:
    source = "> [!TODO] Goal\n> Clarify the objective before details.\n"
    document = _parse(language_pack, source)
    context = RuleContext(
        research_profile, language_pack, FeatureStore(document, document.indexes)
    )
    rule = registry.instantiate(research_profile.rules["terminology.acronym_burden"])
    violations = rule.check(document, context)
    assert violations == []


def test_acronym_burden_accepts_custom_ignore_sentence_pattern(
    registry, language_pack
) -> None:
    config = parse_project_config(
        {
            "rules": {
                "active": ["terminology.acronym_burden"],
                "overrides": {
                    "terminology.acronym_burden": {
                        "options": {"ignore_sentence_patterns": [r"^Tag: [A-Z]{2,}$"]}
                    }
                },
            }
        }
    )
    profile = ProfileResolver(registry).resolve(config, language_pack)
    source = "Tag: ABC\n"
    document = _parse(language_pack, source)
    context = RuleContext(
        profile, language_pack, FeatureStore(document, document.indexes)
    )
    rule = registry.instantiate(profile.rules["terminology.acronym_burden"])
    violations = rule.check(document, context)
    assert violations == []
