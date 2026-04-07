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
    RuleEvidence,
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


class ContextFlagsRule(SourcePatternRule):
    metadata = RuleMetadata(
        rule_id="test.context_flags",
        label="Context capability flags rule",
        layer=Layer.SURFACE_STYLE,
        tractability=Tractability.CLASS_A,
        kind=RuleKind.DIAGNOSTIC_METRIC,
        default_severity=Severity.INFO,
        supported_languages=frozenset({"en"}),
    )

    def check_source(self, lines, doc, ctx):  # noqa: ARG002
        return [
            Violation(
                rule_id=self.rule_id,
                message="context flags snapshot",
                span=lines[0].span,
                severity=self.settings.severity,
                layer=self.metadata.layer,
                evidence=RuleEvidence(
                    features={
                        "embeddings_available": ctx.embeddings_available,
                        "debug_mode": ctx.debug_mode,
                        "experimental_rules_enabled": ctx.enable_experimental,
                    }
                ),
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


def test_rule_detector_populates_runtime_capability_flags(
    registry, language_pack
) -> None:
    registry.add(ContextFlagsRule)
    config = parse_project_config(
        {
            "runtime": {"experimental_rules": True},
            "rules": {"active": ["test.context_flags"]},
        }
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
        debug_mode=True,
    )
    assert len(detection.violations) == 1
    evidence = detection.violations[0].evidence
    assert evidence is not None
    assert evidence.features["embeddings_available"] is False
    assert evidence.features["debug_mode"] is True
    assert evidence.features["experimental_rules_enabled"] is True
