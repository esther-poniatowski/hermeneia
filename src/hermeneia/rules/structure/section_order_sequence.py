"""Detect section-order patterns that invert reader decision sequence."""

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
from hermeneia.rules.common import text_has_marker


class SectionOrderSequenceRule(HeuristicSemanticRule):
    """Sectionordersequencerule."""

    metadata = RuleMetadata(
        rule_id="structure.section_order_sequence",
        label="Section ordering should follow reader decision sequence",
        layer=Layer.DOCUMENT_STRUCTURE,
        tractability=Tractability.CLASS_H,
        kind=RuleKind.DIAGNOSTIC_METRIC,
        default_severity=Severity.INFO,
        supported_languages=frozenset({"en"}),
        evidence_fields=("issue", "offending_heading", "expected_before"),
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
        headings = [
            block
            for block in doc.iter_blocks()
            if block.kind == BlockKind.HEADING and block.sentences
        ]
        if len(headings) < 2:
            return []
        heading_rows = [
            (index, heading, _heading_text(heading))
            for index, heading in enumerate(
                sorted(headings, key=lambda block: block.span.start)
            )
        ]
        purpose = _first_match(
            heading_rows,
            tuple(ctx.language_pack.lexicons.purpose_heading_markers),
        )
        installation = _first_match(
            heading_rows,
            tuple(ctx.language_pack.lexicons.installation_heading_markers),
        )
        usage = _first_match(
            heading_rows,
            tuple(ctx.language_pack.lexicons.usage_heading_markers),
        )
        configuration = _first_match(
            heading_rows,
            tuple(ctx.language_pack.lexicons.configuration_heading_markers),
        )
        advanced = _first_match(
            heading_rows,
            tuple(ctx.language_pack.lexicons.advanced_heading_markers),
        )

        violations: list[Violation] = []
        violations.extend(
            _order_violation(self, installation, purpose, "purpose_over_installation")
        )
        violations.extend(_order_violation(self, usage, purpose, "purpose_over_usage"))
        violations.extend(
            _order_violation(self, configuration, usage, "usage_over_configuration")
        )
        violations.extend(
            _order_violation(self, advanced, usage, "usage_over_advanced")
        )
        return violations


def _heading_text(heading) -> str:
    """Heading text."""
    return " ".join(sentence.projection.text for sentence in heading.sentences).strip()


def _first_match(heading_rows, markers: tuple[str, ...]):
    """First match."""
    if not markers:
        return None
    for index, heading, text in heading_rows:
        if text_has_marker(text, markers):
            return index, heading, text
    return None


def _order_violation(
    rule: SectionOrderSequenceRule,
    left,
    right,
    issue: str,
) -> list[Violation]:
    """Order violation."""
    if left is None or right is None:
        return []
    left_index, left_heading, left_text = left
    right_index, _right_heading, right_text = right
    if left_index > right_index:
        return []
    return [
        Violation(
            rule_id=rule.rule_id,
            message=(
                "Section order inverts reader sequence: "
                f"'{left_text}' appears before '{right_text}'."
            ),
            span=left_heading.span,
            severity=rule.settings.severity,
            layer=rule.metadata.layer,
            evidence=RuleEvidence(
                features={
                    "issue": issue,
                    "offending_heading": left_text.lower(),
                    "expected_before": right_text.lower(),
                }
            ),
            confidence=0.74,
            rationale=(
                "Reader-sequence checks compare coarse heading categories only when both categories are present."
            ),
            rewrite_tactics=(
                "Reorder sections so purpose and usage context appear before "
                "installation/configuration/advanced material.",
            ),
        )
    ]


def register(registry) -> None:
    """Register.

    Parameters
    ----------
    registry : object
        Rule registry used to resolve implementations.
    """
    registry.add(SectionOrderSequenceRule)
