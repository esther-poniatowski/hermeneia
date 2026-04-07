from __future__ import annotations

from pathlib import Path

from hermeneia.document.indexes import FeatureStore
from hermeneia.document.markdown import MarkdownDocumentParser
from hermeneia.document.parser import ParseRequest
from hermeneia.rules.base import RuleContext


def test_heading_parallelism_scopes_to_sibling_groups(
    registry, language_pack, research_profile
) -> None:
    source = """# Alpha

## Setup

## Implementation

# Beta

## Why this matters

## How to interpret
"""
    document = MarkdownDocumentParser(language_pack).parse(
        ParseRequest(source=source, path=Path("demo.md"))
    )
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["structure.heading_parallelism"])
    assert rule.check(document, context) == []


def test_heading_parallelism_reports_mismatch_within_group(
    registry, language_pack, research_profile
) -> None:
    source = """# Alpha

## Setup

## How this works
"""
    document = MarkdownDocumentParser(language_pack).parse(
        ParseRequest(source=source, path=Path("demo.md"))
    )
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["structure.heading_parallelism"])
    violations = rule.check(document, context)
    assert len(violations) == 1
    assert violations[0].rule_id == "structure.heading_parallelism"
