"""Rule dispatch over a parsed, annotated document.

Classes
-------
RuleDiagnostic
    Public API symbol.
DetectionResult
    Public API symbol.
RuleDetector
    Public API symbol.
"""

from __future__ import annotations

from dataclasses import dataclass

from hermeneia.engine.registry import RuleRegistry
from hermeneia.rules.base import (
    BaseRule,
    ResolvedProfile,
    RuntimeCapabilities,
    RuleContext,
    SuggestionMode,
    Tractability,
    Violation,
)
from hermeneia.document.model import Document
from hermeneia.document.indexes import FeatureStore
from hermeneia.language.base import LanguagePack

COMMA_SEPARATOR = ", "


@dataclass(frozen=True)
class RuleDiagnostic:
    """Rulediagnostic."""

    code: str
    rule_id: str
    message: str


@dataclass(frozen=True)
class DetectionResult:
    """Detectionresult."""

    violations: tuple[Violation, ...]
    diagnostics: tuple[RuleDiagnostic, ...] = ()


class RuleDetector:
    """Ruledetector.

    Parameters
    ----------
    registry : RuleRegistry
        Rule registry used to resolve implementations.
    """

    def __init__(self, registry: RuleRegistry) -> None:
        """Initialize the instance."""
        self._registry = registry

    def detect(
        self,
        document: Document,
        profile: ResolvedProfile,
        language_pack: LanguagePack,
        features: FeatureStore,
        debug_mode: bool = False,
    ) -> DetectionResult:
        """Detect.

        Parameters
        ----------
        document : Document
            Document instance to inspect.
        profile : ResolvedProfile
            Resolved profile controlling rule behavior.
        language_pack : LanguagePack
            Input value for ``language_pack``.
        features : FeatureStore
            Input value for ``features``.
        debug_mode : bool
            Input value for ``debug_mode``.

        Returns
        -------
        DetectionResult
            Resulting value produced by this call.
        """
        context = RuleContext(
            profile=profile,
            language_pack=language_pack,
            features=features,
            capabilities=RuntimeCapabilities(
                embeddings_available=features.embeddings_available,
                debug_mode=debug_mode,
                experimental_rules_enabled=profile.enable_experimental,
            ),
        )
        violations: list[Violation] = []
        diagnostics: list[RuleDiagnostic] = []
        # Defensive boundary: rule modules are extension points.
        # pylint: disable=broad-exception-caught
        for settings in profile.active_rules():
            try:
                rule = self._registry.instantiate(settings)
            except Exception as exc:  # pragma: no cover
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
            for violation in rule_violations:
                issue = _validate_violation_contract(rule, violation)
                if issue is not None:
                    diagnostics.append(
                        RuleDiagnostic(
                            code="rule_contract_error",
                            rule_id=rule.rule_id,
                            message=issue,
                        )
                    )
                    continue
                violations.append(violation)
        ordered_violations = tuple(
            sorted(
                violations,
                key=lambda violation: (violation.span.start, violation.rule_id),
            )
        )
        return DetectionResult(
            violations=ordered_violations, diagnostics=tuple(diagnostics)
        )


def _validate_violation_contract(rule: BaseRule, violation: Violation) -> str | None:
    """Validate violation contract."""
    metadata = rule.metadata
    if violation.rule_id != metadata.rule_id:
        return (
            f"violation rule_id '{violation.rule_id}' does not match metadata id "
            f"'{metadata.rule_id}'"
        )
    if violation.layer != metadata.layer:
        return (
            f"violation layer '{violation.layer.value}' does not match metadata layer "
            f"'{metadata.layer.value}'"
        )
    if metadata.evidence_fields:
        if violation.evidence is None:
            return "violation is missing evidence required by rule metadata"
        missing = [
            field
            for field in metadata.evidence_fields
            if field not in violation.evidence.features
        ]
        if missing:
            return (
                "violation evidence is missing required fields: "
                f"{COMMA_SEPARATOR.join(missing)}"
            )
    if metadata.tractability == Tractability.CLASS_H:
        if violation.evidence is None:
            return "class_h violation must include evidence"
        if violation.confidence is None:
            return "class_h violation must include confidence"
    if violation.confidence is not None and not 0.0 <= violation.confidence <= 1.0:
        return "violation confidence must be between 0.0 and 1.0"
    if metadata.suggestion_mode == SuggestionMode.NONE and violation.rewrite_tactics:
        return "rule with suggestion_mode='none' emitted rewrite tactics"
    return None
