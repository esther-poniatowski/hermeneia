"""Application-layer rule registry."""

from __future__ import annotations

from dataclasses import dataclass

from hermeneia.rules.base import BaseRule, ResolvedRuleSettings, RuleMetadata


@dataclass(frozen=True)
class RuleRegistration:
    metadata: RuleMetadata
    rule_cls: type[BaseRule]


class RuleRegistry:
    def __init__(self) -> None:
        self._registrations: dict[str, RuleRegistration] = {}

    def add(self, rule_cls: type[BaseRule]) -> None:
        metadata = rule_cls.metadata
        if metadata.rule_id in self._registrations:
            raise ValueError(f"Rule '{metadata.rule_id}' is already registered")
        self._registrations[metadata.rule_id] = RuleRegistration(
            metadata=metadata, rule_cls=rule_cls
        )

    def get(self, rule_id: str) -> RuleRegistration:
        try:
            return self._registrations[rule_id]
        except KeyError as exc:
            raise KeyError(f"Unknown rule id '{rule_id}'") from exc

    def instantiate(self, settings: ResolvedRuleSettings) -> BaseRule:
        return self.get(settings.metadata.rule_id).rule_cls(settings)

    def all(self) -> tuple[RuleRegistration, ...]:
        return tuple(self._registrations.values())

    def rule_ids(self) -> tuple[str, ...]:
        return tuple(sorted(self._registrations))

    def __contains__(self, rule_id: object) -> bool:
        return isinstance(rule_id, str) and rule_id in self._registrations
