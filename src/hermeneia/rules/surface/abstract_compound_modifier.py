"""Detect abstract compound modifiers that hide explicit relations."""

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
from hermeneia.rules.common import line_text_outside_excluded
from hermeneia.rules.patterns import compile_hyphen_suffix_regex

STACKED_COMPOUND_RE = re.compile(
    r"\b(?:[A-Za-z][A-Za-z0-9]*-[A-Za-z][A-Za-z0-9]*\s+){2,}[A-Za-z][A-Za-z0-9-]*\b",
    re.IGNORECASE,
)


class AbstractCompoundModifierRule(SourcePatternRule):
    metadata = RuleMetadata(
        rule_id="surface.abstract_compound_modifier",
        label="Replace abstract compound modifiers with explicit relations",
        layer=Layer.SURFACE_STYLE,
        tractability=Tractability.CLASS_A,
        kind=RuleKind.HARD_CONSTRAINT,
        default_severity=Severity.ERROR,
        supported_languages=frozenset({"en"}),
        evidence_fields=("compound", "signal"),
    )

    def check_source(self, lines, doc, ctx):
        _ = doc, ctx
        suffixes = tuple(ctx.language_pack.lexicons.abstract_compound_suffixes)
        hyphen_suffix_pattern = compile_hyphen_suffix_regex(suffixes)
        spaced_suffix_pattern = _compile_spaced_suffix_pattern(suffixes)
        patterns = (
            ("hyphen_suffix", hyphen_suffix_pattern),
            ("spaced_suffix", spaced_suffix_pattern),
            ("stacked_compound_chain", STACKED_COMPOUND_RE),
        )
        violations: list[Violation] = []
        seen: set[tuple[int, int]] = set()
        for line in lines:
            if any(kind.value in {"code_block"} for kind in line.container_kinds):
                continue
            probe = line_text_outside_excluded(line)
            for signal, pattern in patterns:
                for match in pattern.finditer(probe):
                    key = (match.start(), match.end())
                    if key in seen:
                        continue
                    seen.add(key)
                    compound = match.group(0)
                    violations.append(
                        Violation(
                            rule_id=self.rule_id,
                            message=(
                                f"Compound modifier '{compound}' is abstract; state the dependency "
                                "or criterion explicitly."
                            ),
                            span=_match_span(line, match.start(), match.end()),
                            severity=self.settings.severity,
                            layer=self.metadata.layer,
                            evidence=RuleEvidence(
                                features={"compound": compound.lower(), "signal": signal}
                            ),
                            confidence=0.88 if signal != "stacked_compound_chain" else 0.92,
                            rewrite_tactics=(
                                "Rewrite the compound as a clause that states what depends on what, and how.",
                            ),
                        )
                    )
        return violations


def _compile_spaced_suffix_pattern(suffixes: tuple[str, ...]) -> re.Pattern[str]:
    normalized_suffixes = tuple(
        suffix.strip().lower() for suffix in suffixes if suffix and suffix.strip()
    )
    if not normalized_suffixes:
        return re.compile(r"(?!x)x")
    suffix_body = "|".join(re.escape(suffix) for suffix in normalized_suffixes)
    return re.compile(
        rf"\b[A-Za-z][A-Za-z0-9-]*\s+(?:{suffix_body})\s+[A-Za-z][A-Za-z0-9-]*\b",
        re.IGNORECASE,
    )


def _match_span(line, start: int, end: int) -> Span:
    return Span(
        start=line.span.start + start,
        end=line.span.start + end,
        start_line=line.span.start_line,
        start_column=line.span.start_column + start,
        end_line=line.span.start_line,
        end_column=line.span.start_column + end,
    )


def register(registry) -> None:
    registry.add(AbstractCompoundModifierRule)
