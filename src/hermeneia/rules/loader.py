"""Built-in and external rule loading."""

from __future__ import annotations

import importlib
import pkgutil

from hermeneia.engine.registry import RuleRegistry
import hermeneia.rules as rules_package


def load_builtin_rules(registry: RuleRegistry) -> None:
    """Walk the built-in rule packages and call register(registry) where present."""

    prefix = f"{rules_package.__name__}."
    for module_info in pkgutil.walk_packages(rules_package.__path__, prefix):
        if module_info.ispkg:
            continue
        module = importlib.import_module(module_info.name)
        register = getattr(module, "register", None)
        if callable(register):
            register(registry)


def load_external_rules(module_name: str, registry: RuleRegistry) -> None:
    """Load a plugin module exposing the same register(registry) protocol."""

    module = importlib.import_module(module_name)
    register = getattr(module, "register", None)
    if not callable(register):
        raise TypeError(f"External rule module '{module_name}' does not export register(registry)")
    register(registry)
