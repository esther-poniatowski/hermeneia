"""Heading-slug link checks."""

from __future__ import annotations

import re

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

SLUG_FRAGMENT_RE = re.compile(r"^[A-Za-z][A-Za-z0-9-]*$")


class HeadingLinkRule(SourcePatternRule):
    metadata = RuleMetadata(
        rule_id="surface.heading_link",
        label="Avoid heading-slug fragments in markdown links",
        layer=Layer.SURFACE_STYLE,
        tractability=Tractability.CLASS_A,
        kind=RuleKind.HARD_CONSTRAINT,
        default_severity=Severity.ERROR,
        supported_languages=frozenset({"en"}),
        evidence_fields=("target",),
    )

    def check_source(self, lines, doc, ctx):
        _ = ctx
        violations: list[Violation] = []
        for line in lines:
            if any(kind.value == "code_block" for kind in line.container_kinds):
                continue
            for span in line.excluded_spans:
                target = doc.source[span.start : span.end].strip()
                if not target or target.startswith(("http://", "https://")):
                    continue
                if "#" not in target:
                    continue
                fragment = target.rsplit("#", 1)[1].strip()
                if not fragment or fragment.startswith("^"):
                    continue
                if SLUG_FRAGMENT_RE.fullmatch(fragment) is None:
                    continue
                violations.append(
                    Violation(
                        rule_id=self.rule_id,
                        message=(
                            "Link target uses a heading-slug fragment; use a block anchor "
                            "target ('#^...') instead."
                        ),
                        span=span,
                        severity=self.settings.severity,
                        layer=self.metadata.layer,
                        evidence=RuleEvidence(features={"target": target}),
                        rewrite_tactics=(
                            "Assign and reference explicit block anchors instead of heading slugs.",
                        ),
                    )
                )
                break
        return violations


def register(registry) -> None:
    registry.add(HeadingLinkRule)

