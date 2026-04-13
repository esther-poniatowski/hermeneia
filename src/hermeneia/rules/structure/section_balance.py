"""Section-balance heuristics."""

from __future__ import annotations

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


class SectionBalanceRule(HeuristicSemanticRule):
    """Sectionbalancerule."""

    metadata = RuleMetadata(
        rule_id="structure.section_balance",
        label="Section lengths are strongly imbalanced",
        layer=Layer.DOCUMENT_STRUCTURE,
        tractability=Tractability.CLASS_H,
        kind=RuleKind.DIAGNOSTIC_METRIC,
        default_severity=Severity.INFO,
        supported_languages=frozenset({"en"}),
        default_options={"max_ratio": 3.5},
        evidence_fields=("largest_words", "smallest_words", "ratio"),
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
        max_ratio = self.settings.float_option("max_ratio", 3.5)
        sections = [
            section
            for section in ctx.features.sections
            if section.heading_block_id is not None
        ]
        if len(sections) < 2:
            return []
        section_words = {
            section.heading_block_id: _section_word_count(doc, section.block_ids)
            for section in sections
            if section.heading_block_id is not None
        }
        nonzero = {
            section_id: count
            for section_id, count in section_words.items()
            if count > 0
        }
        if len(nonzero) < 2:
            return []
        largest_id, largest_words = max(nonzero.items(), key=lambda item: item[1])
        smallest_id, smallest_words = min(nonzero.items(), key=lambda item: item[1])
        ratio = largest_words / smallest_words
        if ratio <= max_ratio:
            return []
        largest_heading = doc.block_by_id(largest_id)
        if largest_heading is None:
            return []
        return [
            Violation(
                rule_id=self.rule_id,
                message="Section length distribution is imbalanced relative to sibling sections.",
                span=largest_heading.span,
                severity=self.settings.severity,
                layer=self.metadata.layer,
                evidence=RuleEvidence(
                    features={
                        "largest_section_id": largest_id,
                        "smallest_section_id": smallest_id,
                        "largest_words": largest_words,
                        "smallest_words": smallest_words,
                        "ratio": round(ratio, 3),
                    },
                    score=ratio,
                    threshold=max_ratio,
                ),
                confidence=0.62,
                rationale="Section-balance checks compare only coarse word-count ratios across declared sections.",
                rewrite_tactics=(
                    "Redistribute supporting material so major sections carry comparable argumentative load.",
                ),
            )
        ]


def _section_word_count(doc, block_ids: tuple[str, ...]) -> int:
    """Section word count."""
    total = 0
    for block_id in block_ids:
        block = doc.block_by_id(block_id)
        if block is None:
            continue
        for sentence in block.sentences:
            total += len(sentence.projection.text.split())
    return total


def register(registry) -> None:
    """Register.

    Parameters
    ----------
    registry : object
        Rule registry used to resolve implementations.
    """
    registry.add(SectionBalanceRule)
