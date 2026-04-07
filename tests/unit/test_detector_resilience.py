from __future__ import annotations

from pathlib import Path

from hermeneia.config.profile import ProfileResolver
from hermeneia.config.schema import parse_project_config
from hermeneia.document.indexes import FeatureStore
from hermeneia.document.markdown import MarkdownDocumentParser
from hermeneia.document.parser import ParseRequest
from hermeneia.engine.detector import RuleDetector
from hermeneia.rules.base import (
    Layer,
    RuleKind,
    RuleMetadata,
    Severity,
    SourcePatternRule,
    Tractability,
)


class BrokenRule(SourcePatternRule):
    metadata = RuleMetadata(
        rule_id="test.broken",
        label="Broken test rule",
        layer=Layer.SURFACE_STYLE,
        tractability=Tractability.CLASS_A,
        kind=RuleKind.SOFT_HEURISTIC,
        default_severity=Severity.INFO,
        supported_languages=frozenset({"en"}),
    )

    def check_source(self, lines, doc, ctx):  # noqa: ARG002
        raise RuntimeError("synthetic rule failure")


def test_rule_detector_contains_rule_exceptions(registry, language_pack) -> None:
    registry.add(BrokenRule)
    config = parse_project_config({"rules": {"active": ["surface.contraction", "test.broken"]}})
    profile = ProfileResolver(registry).resolve(config, language_pack)
    document = MarkdownDocumentParser(language_pack).parse(
        ParseRequest(source="It's fine.\n", path=Path("demo.md"))
    )
    detection = RuleDetector(registry).detect(
        document,
        profile,
        language_pack,
        FeatureStore(document, document.indexes),
    )
    assert any(violation.rule_id == "surface.contraction" for violation in detection.violations)
    assert any(
        diagnostic.rule_id == "test.broken" and diagnostic.code == "rule_execution_error"
        for diagnostic in detection.diagnostics
    )
