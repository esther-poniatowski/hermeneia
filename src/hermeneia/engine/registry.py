"""Application-layer rule registry."""

from __future__ import annotations

from dataclasses import dataclass

from hermeneia.rules.base import BaseRule, ResolvedRuleSettings, RuleMetadata


@dataclass(frozen=True)
class RuleRegistration:
    """Ruleregistration."""

    metadata: RuleMetadata
    rule_cls: type[BaseRule]


class RuleRegistry:
    """Ruleregistry."""

    def __init__(self) -> None:
        """Initialize the instance."""
        self._registrations: dict[str, RuleRegistration] = {}

    def add(self, rule_cls: type[BaseRule]) -> None:
        """Add.

        Parameters
        ----------
        rule_cls : type[BaseRule]
            Input value for ``rule_cls``.
        """
        metadata = rule_cls.metadata
        if metadata.rule_id in self._registrations:
            raise ValueError(f"Rule '{metadata.rule_id}' is already registered")
        self._registrations[metadata.rule_id] = RuleRegistration(
            metadata=metadata, rule_cls=rule_cls
        )

    def get(self, rule_id: str) -> RuleRegistration:
        """Get.

        Parameters
        ----------
        rule_id : str
            Input value for ``rule_id``.

        Returns
        -------
        RuleRegistration
            Resulting value produced by this call.
        """
        try:
            return self._registrations[rule_id]
        except KeyError as exc:
            raise KeyError(f"Unknown rule id '{rule_id}'") from exc

    def instantiate(self, settings: ResolvedRuleSettings) -> BaseRule:
        """Instantiate.

        Parameters
        ----------
        settings : ResolvedRuleSettings
            Input value for ``settings``.

        Returns
        -------
        BaseRule
            Resulting value produced by this call.
        """
        return self.get(settings.metadata.rule_id).rule_cls(settings)

    def all(self) -> tuple[RuleRegistration, ...]:
        """All.

        Returns
        -------
        tuple[RuleRegistration, ...]
            Resulting value produced by this call.
        """
        return tuple(self._registrations.values())

    def rule_ids(self) -> tuple[str, ...]:
        """Rule ids.

        Returns
        -------
        tuple[str, ...]
            Resulting value produced by this call.
        """
        return tuple(sorted(self._registrations))

    def __contains__(self, rule_id: object) -> bool:
        """Contains."""
        return isinstance(rule_id, str) and rule_id in self._registrations
