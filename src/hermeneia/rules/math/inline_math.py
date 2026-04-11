"""Equation-like inline-math checks."""

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

INLINE_ATOM_RE = re.compile(r"[A-Za-z][A-Za-z0-9']*")
INLINE_NUMERIC_RE = re.compile(r"[+-]?\d+(?:\.\d+)?")
INLINE_LATEX_ATOM_RE = re.compile(
    r"\\(?:mathbf|boldsymbol|mathbb|mathrm)\{[A-Za-z0-9]+\}"
)
INLINE_ALLOWED_RE = re.compile(r"[A-Za-z0-9\\_^{}()\[\]|,.'\s:/+-]+")


class InlineMathRule(SourcePatternRule):
    metadata = RuleMetadata(
        rule_id="math.inline_math",
        label="Avoid equation-like inline math when display math is clearer",
        layer=Layer.SURFACE_STYLE,
        tractability=Tractability.CLASS_A,
        kind=RuleKind.SOFT_HEURISTIC,
        default_severity=Severity.WARNING,
        supported_languages=frozenset({"en"}),
        default_options={"max_inline_length": 40},
        evidence_fields=("reason", "expression"),
    )

    def check_source(self, lines, doc, ctx):
        _ = ctx
        max_inline_length = self.settings.int_option("max_inline_length", 40)
        violations: list[Violation] = []
        for line in lines:
            context_kinds = {kind.value for kind in line.container_kinds}
            if "code_block" in context_kinds:
                continue
            if context_kinds & {"table_cell", "block_quote", "admonition", "list_item"}:
                continue
            for span in line.excluded_spans:
                raw_fragment = doc.source[span.start : span.end]
                if not _is_inline_math_fragment(raw_fragment):
                    continue
                content = raw_fragment[1:-1].strip()
                if not content:
                    continue
                has_equality = "=" in content
                if has_equality and _is_trivial_inline_equality(content):
                    continue
                if has_equality:
                    reason = "equation_like"
                elif "\\frac" in content:
                    reason = "fraction_like"
                elif len(content) > max_inline_length:
                    reason = "long_expression"
                else:
                    continue
                violations.append(
                    Violation(
                        rule_id=self.rule_id,
                        message=(
                            "Inline math carries equation-level content; prefer an explanatory "
                            "lead-in and a display equation."
                        ),
                        span=span,
                        severity=self.settings.severity,
                        layer=self.metadata.layer,
                        evidence=RuleEvidence(
                            features={"reason": reason, "expression": content}
                        ),
                        rewrite_tactics=(
                            "Move the expression into a '$$...$$' block and introduce it in prose.",
                        ),
                    )
                )
                break
        return violations


def _is_inline_math_fragment(text: str) -> bool:
    if not text.startswith("$") or not text.endswith("$"):
        return False
    if text.startswith("$$") or text.endswith("$$"):
        return False
    return text.count("$") >= 2


def _has_binary_minus(text: str) -> bool:
    for index, char in enumerate(text):
        if char != "-":
            continue
        previous_index = index - 1
        while previous_index >= 0 and text[previous_index].isspace():
            previous_index -= 1
        previous = text[previous_index] if previous_index >= 0 else None
        if previous is None or previous in {"(", "[", "{", ",", "^", "_"}:
            continue
        return True
    return False


def _is_simple_inline_expression(expression: str) -> bool:
    if len(expression) > 60:
        return False
    if "\\frac" in expression or "\\sum" in expression or "\\int" in expression:
        return False
    if "+" in expression:
        return False
    if _has_binary_minus(expression):
        return False
    return bool(INLINE_ALLOWED_RE.fullmatch(expression))


def _is_trivial_inline_equality(content: str) -> bool:
    stripped = content.strip()
    eq_count = stripped.count("=")
    if not eq_count:
        return False

    if eq_count >= 2 and ":=" not in stripped:
        parts = [part.strip() for part in stripped.split("=")]
        if all(parts) and all(_is_simple_inline_expression(part) for part in parts):
            return True

    if eq_count != 1:
        return False

    if ":=" in stripped:
        left, right = (part.strip() for part in stripped.split(":=", 1))
    else:
        left, right = (part.strip() for part in stripped.split("=", 1))
    if not left or not right:
        return False

    rhs_is_numeric = bool(INLINE_NUMERIC_RE.fullmatch(right))
    rhs_is_identifier = bool(INLINE_ATOM_RE.fullmatch(right))
    rhs_is_latex_atom = bool(INLINE_LATEX_ATOM_RE.fullmatch(right))

    if rhs_is_numeric or rhs_is_identifier or rhs_is_latex_atom:
        return _is_simple_inline_expression(left)
    return _is_simple_inline_expression(left) and _is_simple_inline_expression(right)


def register(registry) -> None:
    registry.add(InlineMathRule)
