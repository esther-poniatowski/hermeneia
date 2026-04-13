"""Bare-symbol detection for math prose."""

from __future__ import annotations

import re

from hermeneia.document.model import Span
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

BARE_SYMBOL_RE = re.compile(
    r"\b(?:for all|for each|for every|at fixed|at constant|over all|increases with|decreases with|"
    r"a bimodal|an? (?:monotone|decreasing|increasing|bounded|positive|negative|concave|convex))"
    r"\s+\$[^$]{1,12}\$",
    re.IGNORECASE,
)
BARE_PREP_SYMBOL_RE = re.compile(
    r"\b(?:indexed by|a (?:function|subset|restriction|family|object|kernel|map) (?:on|of|over|from|in|into))"
    r"\s+\$[^$]{1,20}\$",
    re.IGNORECASE,
)
BARE_SPACE_SYMBOL_RE = re.compile(
    r"\b(?:on|of|across|over|from|into|in)\s+\$\\(?:Theta|mathcal|Lambda|Omega)\b"
    r"|\b(?:on|of|across|over|from|into|in)\s+\$\\mathbb\{(?!R\})[A-Z]\}",
    re.IGNORECASE,
)


class BareSymbolRule(SourcePatternRule):
    """Baresymbolrule."""

    metadata = RuleMetadata(
        rule_id="math.bare_symbol",
        label="Symbols in qualifier or prepositional position must carry object names",
        layer=Layer.SURFACE_STYLE,
        tractability=Tractability.CLASS_A,
        kind=RuleKind.HARD_CONSTRAINT,
        default_severity=Severity.ERROR,
        supported_languages=frozenset({"en"}),
        evidence_fields=("matched_text",),
    )

    def check_source(self, lines, doc, ctx):
        """Check source.

        Parameters
        ----------
        lines : object
            Source lines involved in this computation.
        doc : object
            Document instance to inspect.
        ctx : object
            Rule evaluation context.

        Returns
        -------
        object
            Resulting value produced by this call.
        """
        violations: list[Violation] = []
        patterns = (BARE_SYMBOL_RE, BARE_PREP_SYMBOL_RE, BARE_SPACE_SYMBOL_RE)
        for line in lines:
            if any(
                kind.value in {"code_block", "display_math"}
                for kind in line.container_kinds
            ):
                continue
            probe = line.text
            for pattern in patterns:
                match = pattern.search(probe)
                if match is None:
                    continue
                violations.append(
                    Violation(
                        rule_id=self.rule_id,
                        message=(
                            "Name the mathematical object before the symbol in this "
                            "qualifier or prepositional phrase."
                        ),
                        span=_match_span(line, match.start(), match.end()),
                        severity=self.settings.severity,
                        layer=self.metadata.layer,
                        evidence=RuleEvidence(
                            features={"matched_text": match.group(0)}
                        ),
                        rewrite_tactics=(
                            "Insert the object name immediately before the symbol.",
                        ),
                    )
                )
                break
        return violations


def _match_span(line, start: int, end: int) -> Span:
    """Match span."""
    return Span(
        start=line.span.start + start,
        end=line.span.start + end,
        start_line=line.span.start_line,
        start_column=line.span.start_column + start,
        end_line=line.span.start_line,
        end_column=line.span.start_column + end,
    )


def register(registry) -> None:
    """Register.

    Parameters
    ----------
    registry : object
        Rule registry used to resolve implementations.
    """
    registry.add(BareSymbolRule)
