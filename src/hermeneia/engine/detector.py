"""Rule dispatch over a parsed, annotated document."""

from __future__ import annotations

from dataclasses import dataclass

from hermeneia.engine.registry import RuleRegistry
from hermeneia.rules.base import ResolvedProfile, RuleContext, Violation
from hermeneia.document.model import Document
from hermeneia.document.indexes import FeatureStore
from hermeneia.language.base import LanguagePack


@dataclass(frozen=True)
class RuleDiagnostic:
    code: str
    rule_id: str
    message: str


@dataclass(frozen=True)
class DetectionResult:
    violations: tuple[Violation, ...]
    diagnostics: tuple[RuleDiagnostic, ...] = ()


class RuleDetector:
    def __init__(self, registry: RuleRegistry) -> None:
        self._registry = registry

    def detect(
        self,
        document: Document,
        profile: ResolvedProfile,
        language_pack: LanguagePack,
        features: FeatureStore,
    ) -> DetectionResult:
        context = RuleContext(
            profile=profile,
            language_pack=language_pack,
            features=features,
            enable_experimental=profile.enable_experimental,
        )
        violations: list[Violation] = []
        diagnostics: list[RuleDiagnostic] = []
        for settings in profile.active_rules():
            try:
                rule = self._registry.instantiate(settings)
            except Exception as exc:  # pragma: no cover - defensive boundary
                diagnostics.append(
                    RuleDiagnostic(
                        code="rule_instantiation_error",
                        rule_id=settings.metadata.rule_id,
                        message=str(exc),
                    )
                )
                continue
            try:
                rule_violations = rule.check(document, context)
            except Exception as exc:
                diagnostics.append(
                    RuleDiagnostic(
                        code="rule_execution_error",
                        rule_id=rule.rule_id,
                        message=str(exc),
                    )
                )
                continue
            violations.extend(rule_violations)
        ordered_violations = tuple(
            sorted(violations, key=lambda violation: (violation.span.start, violation.rule_id))
        )
        return DetectionResult(violations=ordered_violations, diagnostics=tuple(diagnostics))
