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
    Violation,
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


class ContractBrokenRule(SourcePatternRule):
    metadata = RuleMetadata(
        rule_id="test.contract_broken",
        label="Contract-broken test rule",
        layer=Layer.SURFACE_STYLE,
        tractability=Tractability.CLASS_A,
        kind=RuleKind.SOFT_HEURISTIC,
        default_severity=Severity.INFO,
        supported_languages=frozenset({"en"}),
        evidence_fields=("required_field",),
    )

    def check_source(self, lines, doc, ctx):  # noqa: ARG002
        return [
            Violation(
                rule_id=self.rule_id,
                message="synthetic contract mismatch",
                span=lines[0].span,
                severity=self.settings.severity,
                layer=self.metadata.layer,
            )
        ]


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


def test_rule_detector_enforces_violation_contract(registry, language_pack) -> None:
    registry.add(ContractBrokenRule)
    config = parse_project_config(
        {"rules": {"active": ["surface.contraction", "test.contract_broken"]}}
    )
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
    assert all(violation.rule_id != "test.contract_broken" for violation in detection.violations)
    assert any(
        diagnostic.rule_id == "test.contract_broken" and diagnostic.code == "rule_contract_error"
        for diagnostic in detection.diagnostics
    )
