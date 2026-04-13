"""Detect heading-level skips in document outline."""

from __future__ import annotations

from hermeneia.document.model import BlockKind
from hermeneia.rules.base import (
    HeuristicSemanticRule,
    Layer,
    RuleEvidence,
    RuleKind,
    RuleMetadata,
    Severity,
    Tractability,
    Violation,
)


class HeadingLevelSkipRule(HeuristicSemanticRule):
    """Headinglevelskiprule."""

    metadata = RuleMetadata(
        rule_id="structure.heading_level_skip",
        label="Heading levels should not skip depth",
        layer=Layer.DOCUMENT_STRUCTURE,
        tractability=Tractability.CLASS_A,
        kind=RuleKind.HARD_CONSTRAINT,
        default_severity=Severity.WARNING,
        supported_languages=frozenset({"en"}),
        evidence_fields=("previous_level", "current_level"),
    )

    def check(self, doc, ctx):
        """Check.

        Parameters
        ----------
        doc : object
            Document instance to inspect.
        ctx : object
            Rule evaluation context.

        Returns
        -------
        object
            Resulting value produced by this call.
        """
        _ = ctx
        headings = [
            block
            for block in doc.iter_blocks()
            if block.kind == BlockKind.HEADING and "level" in block.metadata
        ]
        headings.sort(key=lambda block: block.span.start)
        violations: list[Violation] = []
        previous_level: int | None = None
        for heading in headings:
            level = int(heading.metadata.get("level", 1))
            if previous_level is not None and level > previous_level + 1:
                violations.append(
                    Violation(
                        rule_id=self.rule_id,
                        message=(
                            f"Heading level jumps from H{previous_level} to H{level}; "
                            "insert intermediate heading level."
                        ),
                        span=heading.span,
                        severity=self.settings.severity,
                        layer=self.metadata.layer,
                        evidence=RuleEvidence(
                            features={
                                "previous_level": previous_level,
                                "current_level": level,
                            }
                        ),
                        confidence=0.96,
                        rewrite_tactics=(
                            "Use contiguous heading depths (H1→H2→H3) without skipping levels.",
                        ),
                    )
                )
            previous_level = level
        return violations


def register(registry) -> None:
    """Register.

    Parameters
    ----------
    registry : object
        Rule registry used to resolve implementations.
    """
    registry.add(HeadingLevelSkipRule)
