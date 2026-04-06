from __future__ import annotations

import sys

from hermeneia.rules.loader import load_external_rules
from hermeneia.rules.base import (
    Layer,
    RuleKind,
    RuleMetadata,
    Severity,
    Tractability,
    SourcePatternRule,
)


def test_load_builtin_rules_registers_expected_ids(registry) -> None:
    assert "surface.contraction" in registry.rule_ids()
    assert "math.display_math" in registry.rule_ids()
    assert "paragraph.topic_sentence" in registry.rule_ids()


def test_load_external_rules_uses_same_register_protocol(tmp_path, registry) -> None:
    module_path = tmp_path / "custom_rule_module.py"
    module_path.write_text(
        "\n".join(
            [
                "from hermeneia.rules.base import Layer, RuleKind, RuleMetadata, Severity, Tractability, SourcePatternRule",
                "class DemoRule(SourcePatternRule):",
                "    metadata = RuleMetadata(",
                "        rule_id='demo.rule',",
                "        label='demo',",
                "        layer=Layer.SURFACE_STYLE,",
                "        tractability=Tractability.CLASS_A,",
                "        kind=RuleKind.SOFT_HEURISTIC,",
                "        default_severity=Severity.INFO,",
                "        supported_languages=frozenset({'en'}),",
                "    )",
                "    def check_source(self, lines, doc, ctx):",
                "        return []",
                "def register(registry):",
                "    registry.add(DemoRule)",
            ]
        ),
        encoding="utf-8",
    )
    sys.path.insert(0, str(tmp_path))
    try:
        load_external_rules("custom_rule_module", registry)
    finally:
        sys.path.remove(str(tmp_path))
    assert "demo.rule" in registry.rule_ids()
