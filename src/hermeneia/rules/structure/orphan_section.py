"""Detect orphaned section shells in heading hierarchies."""

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
from hermeneia.rules.common import sentence_word_count


class OrphanSectionRule(HeuristicSemanticRule):
    """Orphansectionrule."""

    metadata = RuleMetadata(
        rule_id="structure.orphan_section",
        label="Avoid orphan section shells",
        layer=Layer.DOCUMENT_STRUCTURE,
        tractability=Tractability.CLASS_H,
        kind=RuleKind.DIAGNOSTIC_METRIC,
        default_severity=Severity.INFO,
        supported_languages=frozenset({"en"}),
        default_options={"min_parent_words": 24},
        evidence_fields=("issue", "direct_children", "parent_words"),
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
        min_parent_words = self.settings.int_option("min_parent_words", 24)
        violations: list[Violation] = []
        for section in ctx.features.sections:
            heading_id = section.heading_block_id
            if heading_id is None:
                continue
            heading = doc.block_by_id(heading_id)
            if heading is None or heading.kind != BlockKind.HEADING:
                continue
            level = int(heading.metadata.get("level", 1))
            direct_children, parent_words = _section_shell_stats(
                doc, section.block_ids, level
            )
            if not direct_children and not parent_words:
                violations.append(
                    _violation(
                        self,
                        heading,
                        issue="empty_section",
                        direct_children=direct_children,
                        parent_words=parent_words,
                    )
                )
                continue
            if direct_children == 1 and parent_words < min_parent_words:
                violations.append(
                    _violation(
                        self,
                        heading,
                        issue="single_child_shell",
                        direct_children=direct_children,
                        parent_words=parent_words,
                    )
                )
        return violations


def _section_shell_stats(
    doc, block_ids: tuple[str, ...], level: int
) -> tuple[int, int]:
    """Section shell stats."""
    direct_children = 0
    parent_words = 0
    before_first_direct_child = True
    for block_id in block_ids[1:]:
        block = doc.block_by_id(block_id)
        if block is None:
            continue
        if block.kind == BlockKind.HEADING:
            block_level = int(block.metadata.get("level", 1))
            if block_level == level + 1:
                direct_children += 1
                before_first_direct_child = False
            continue
        if not before_first_direct_child:
            continue
        for sentence in block.sentences:
            parent_words += sentence_word_count(sentence)
    return direct_children, parent_words


def _violation(
    rule: OrphanSectionRule,
    heading,
    *,
    issue: str,
    direct_children: int,
    parent_words: int,
) -> Violation:
    """Violation."""
    if issue == "empty_section":
        message = "Section has a heading but no substantive content."
    else:
        message = "Section appears as a shell with one direct subsection and minimal parent-level prose."
    return Violation(
        rule_id=rule.rule_id,
        message=message,
        span=heading.span,
        severity=rule.settings.severity,
        layer=rule.metadata.layer,
        evidence=RuleEvidence(
            features={
                "issue": issue,
                "direct_children": direct_children,
                "parent_words": parent_words,
            }
        ),
        confidence=0.72,
        rationale="Orphan-section checks estimate hierarchy shell depth using heading levels and parent prose volume.",
        rewrite_tactics=(
            "Either merge the single-child shell into its child section or add parent-level framing prose.",
        ),
    )


def register(registry) -> None:
    """Register.

    Parameters
    ----------
    registry : object
        Rule registry used to resolve implementations.
    """
    registry.add(OrphanSectionRule)
