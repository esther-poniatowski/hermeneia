"""Rule dispatch over a parsed, annotated document."""

from __future__ import annotations

from hermeneia.engine.registry import RuleRegistry
from hermeneia.rules.base import ResolvedProfile, RuleContext, Violation
from hermeneia.document.model import Document
from hermeneia.document.indexes import FeatureStore
from hermeneia.language.base import LanguagePack


class RuleDetector:
    def __init__(self, registry: RuleRegistry) -> None:
        self._registry = registry

    def detect(
        self,
        document: Document,
        profile: ResolvedProfile,
        language_pack: LanguagePack,
        features: FeatureStore,
    ) -> list[Violation]:
        context = RuleContext(
            profile=profile,
            language_pack=language_pack,
            features=features,
            enable_experimental=profile.enable_experimental,
        )
        violations: list[Violation] = []
        for settings in profile.active_rules():
            rule = self._registry.instantiate(settings)
            violations.extend(rule.check(document, context))
        return sorted(violations, key=lambda violation: (violation.span.start, violation.rule_id))
