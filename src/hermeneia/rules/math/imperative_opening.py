"""Imperative-opening bans for mathematical prose."""

from __future__ import annotations

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
from hermeneia.rules.common import line_text_outside_excluded
from hermeneia.rules.patterns import compile_structured_leading_term_regex


class ImperativeOpeningRule(SourcePatternRule):
    """Imperativeopeningrule."""

    metadata = RuleMetadata(
        rule_id="math.imperative_opening",
        label="Avoid imperative mathematical openings",
        layer=Layer.SURFACE_STYLE,
        tractability=Tractability.CLASS_A,
        kind=RuleKind.HARD_CONSTRAINT,
        default_severity=Severity.ERROR,
        supported_languages=frozenset({"en"}),
        evidence_fields=("verb",),
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
        pattern = compile_structured_leading_term_regex(
            tuple(ctx.language_pack.lexicons.imperative_opening_verbs)
        )
        violations: list[Violation] = []
        for line in lines:
            if any(
                kind.value in {"code_block", "display_math"}
                for kind in line.container_kinds
            ):
                continue
            probe = line_text_outside_excluded(line)
            match = pattern.search(probe)
            if match is None:
                continue
            verb = match.group("term")
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    message=f"Avoid imperative opening '{verb} ...'; name the object or purpose declaratively.",
                    span=_match_span(line, match.start("term"), match.end("term")),
                    severity=self.settings.severity,
                    layer=self.metadata.layer,
                    evidence=RuleEvidence(features={"verb": verb.lower()}),
                    rewrite_tactics=(
                        "State the purpose first, then introduce the object or assumption declaratively.",
                    ),
                )
            )
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
    registry.add(ImperativeOpeningRule)
