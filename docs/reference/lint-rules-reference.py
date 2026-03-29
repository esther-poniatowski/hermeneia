"""
Prototype reference for math-writing lint rules.

This file preserves a pre-refactor linter implementation as source material for
future rule extraction. It is not a supported hermeneia module, not part of the
public API, and not the canonical implementation shape for the project.

The content remains useful because it collects automatable local checks derived
from mathematical writing practice. Rules can be selectively enabled,
disabled, or reconfigured via a YAML override file passed to
:func:`load_config`.

Override file format
--------------------

.. code-block:: yaml

    # Disable specific rule groups
    disabled_rules:
      - first_person
      - contractions

    # Override archive directory names
    archive_dirs:
      - bak
      - to-move
      - old

    # Add project-specific banned transitions
    extra_banned_transitions:
      - "as a consequence"

    # Add project-specific acronyms to flag
    extra_acronyms:
      - "RNN"
      - "MLP"

Checks focus on local, automatable rules:

- Display math should not end with punctuation inside the $$...$$ block.
- Display math should be preceded by a non-empty explanatory line.
- Display math should not be preceded by a content-free lead-in.
- Inline math should not contain equation-like content unless trivial.
- Cross-links should use block anchors (^...), not heading-slug fragments.
- Avoid imperative scaffolding at the start of a line.
- Avoid banned transition scaffolding.
- Avoid first-person pronouns and generic "one can ..." phrasing.
- Avoid contractions.
- Avoid "See [link]" scaffolding.
- Avoid "In the ... case ..." and "the ... case" scaffolding.
- Avoid abstract-framing red-flag phrases.
- Avoid unexplained acronyms.
- Avoid numbered anonymous case splits.
- Do not reference block anchors as raw tokens in running text.
- If end-of-proof symbol is used, require ``*Proof.*`` marker.
- Bare-symbol detection after quantifiers and prepositions.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator

import yaml


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

@dataclass
class LintConfig:
    """Lint configuration with defaults that can be overridden per project."""

    domain: str = "math"
    disabled_rules: set[str] = field(default_factory=set)
    archive_dirs: set[str] = field(default_factory=lambda: {"bak", "to-move"})
    extra_banned_transitions: list[str] = field(default_factory=list)
    extra_acronyms: list[str] = field(default_factory=list)


def load_config(path: Path) -> LintConfig:
    """Load lint configuration from a YAML override file."""
    if not path.exists():
        print(f"Warning: config file not found: {path}", file=sys.stderr)
        return LintConfig()

    with open(path, encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}

    return LintConfig(
        domain=raw.get("domain", "math"),
        disabled_rules=set(raw.get("disabled_rules", [])),
        archive_dirs=set(raw.get("archive_dirs", ["bak", "to-move"])),
        extra_banned_transitions=raw.get("extra_banned_transitions", []),
        extra_acronyms=raw.get("extra_acronyms", []),
    )


# ---------------------------------------------------------------------------
# Issue type
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Issue:
    path: Path
    line: int
    rule: str
    message: str


# ---------------------------------------------------------------------------
# Compiled patterns
# ---------------------------------------------------------------------------

FENCE_RE = re.compile(r"^\s*(```+|~~~+)")
HEADING_RE = re.compile(r"^\s*#{1,6}\s+")

INLINE_MATH_RE = re.compile(r"(?<!\\)\$(?!\$)(.+?)(?<!\\)\$")
INLINE_CODE_RE = re.compile(r"`[^`]*`")

HEADING_LINK_RE = re.compile(r"\]\((?!https?://)[^)]*#(?!\^)[a-z][^)]*\)")

IMPERATIVE_START_RE = re.compile(
    r"^\s*(?:>\s*)*(?:(?:[-*+])\s+|\d+\.\s+)?(Define|Assume|Write|Let|Denote|Set|Fix)\b"
)
NUMBERED_CASE_RE = re.compile(r"\b[Cc]ase\s+\d+\b")

SEE_LINK_RE = re.compile(r"\bsee\b\s*:?\s*\[", re.IGNORECASE)
IN_THE_CASE_START_RE = re.compile(
    r"^\s*(?:>\s*)*(?:(?:[-*+])\s+|\d+\.\s+)?In the (?!worst |best |base |general |special )[^,\n]{1,80} case\b"
)
THE_CASE_NP_RE = re.compile(
    r"\bthe\s+(?!this\b|that\b|each\b|above\b|following\b|general\b|special\b|worst\b|best\b|base\b)"
    r"[a-z][a-z-]*(?:\s+[a-z][a-z-]*)?\s+case\b",
    re.IGNORECASE,
)
ROLE_OF_RE = re.compile(r"\bthe role of\b", re.IGNORECASE)
NATURE_OF_RE = re.compile(r"\bthe nature of the\b", re.IGNORECASE)
TREATMENT_OF_RE = re.compile(r"\btreatments? of\b", re.IGNORECASE)
ACRONYM_RE = re.compile(r"\b(?:IVT|WTA)\b")

BANNED_TRANSITION_START_RE = re.compile(
    r"^\s*(?:>\s*)*(?:(?:[-*+])\s+|\d+\.\s+)?"
    r"(?:"
    r"equivalently|more explicitly|this gives|rewriting|note that|notice that|recall that|observe that|"
    r"clearly|obviously|naturally|of course|straightforward(?:ly)?|it can be shown|it is easy to see|it follows that"
    r")\b",
    re.IGNORECASE,
)
CONTENT_FREE_LEADIN_RE = re.compile(
    r"^(?:therefore|hence|then|this gives|more explicitly|equivalently|rewriting)\s*:?\s*$",
    re.IGNORECASE,
)
FIRST_PERSON_RE = re.compile(r"\b(?:we|We|our|Our|us|Us)\b")
LET_US_RE = re.compile(r"\b(?:let us|Let us)\b")
GENERIC_ONE_RE = re.compile(r"\b(?:one|One)\s+(?:can|could|may|might|should|would|will|must)\b")
CONTRACTION_RE = re.compile(
    r"\b(?:"
    r"it's|that's|there's|here's|let's|"
    r"can't|won't|don't|doesn't|didn't|isn't|aren't|wasn't|weren't|"
    r"haven't|hasn't|hadn't|wouldn't|shouldn't|couldn't|"
    r"i'm|i've|i'll|"
    r"you're|you've|you'll|"
    r"we're|we've|we'll|"
    r"they're|they've|they'll"
    r")\b",
    re.IGNORECASE,
)
IN_WAYS_RE = re.compile(
    r"\bin\s+(?:various|different|several|many|distinct|important|meaningful|significant|"
    r"structure-specific|architecture-specific)\s+ways\b|\bin\s+ways\s+that\b",
    re.IGNORECASE,
)
GIVEN_BY_RE = re.compile(r"\bgiven by\b", re.IGNORECASE)
OF_ORDER_RE = re.compile(r"\bof order\b", re.IGNORECASE)
FIXED_TO_RE = re.compile(r"\bfixed to\b", re.IGNORECASE)
GENERIC_LINK_TEXT_RE = re.compile(
    r"\[(?:Lemma|Result|Proposition|Theorem|Corollary)\s*\([^\]]+\)\]\([^)]*\)"
)

ANCHOR_TOKEN_RE = re.compile(r"\^[a-z][a-z0-9]*-[a-z0-9-]+")
LINK_DEST_RE = re.compile(r"\]\([^)]*\)")

TIMES_WORD_RE = re.compile(r"(?<!\\)\btimes\b")
MULTIPLIED_BY_RE = re.compile(r"\bmultiplied by\b", re.IGNORECASE)
CONVERGES_TO_ONE_RE = re.compile(r"\bconverges to (?:one|1|\$1\$)\b", re.IGNORECASE)
INLINE_MATH_IS_ZERO_RE = re.compile(r"\$[^$]+\$\s+is\s+zero\b", re.IGNORECASE)

RHO_INPUT_MAG_RE = re.compile(r"\\rho\s*:?=\s*\\\|\\mathbf\{u\}\\\|")
SQUARE_RE = re.compile(r"\\square\b")
PROOF_MARKER_RE = re.compile(r"\*Proof\.\*")

BARE_SYMBOL_RE = re.compile(
    r"\b(?:for all|for each|for every|at fixed|at constant|over all|increases with|decreases with|"
    r"a bimodal|an? (?:monotone|decreasing|increasing|bounded|positive|negative|concave|convex))"
    r"\s+\$[^$]{1,12}\$"
)
BARE_PREP_SYMBOL_RE = re.compile(
    r"\b(?:indexed by|a (?:function|subset|restriction|family|object|kernel|map) (?:on|of|over|from|in|into))"
    r"\s+\$[^$]{1,20}\$"
)
BARE_SPACE_SYMBOL_RE = re.compile(
    r"\b(?:on|of|across|over|from|into|in)\s+\$\\(?:Theta|mathcal|Lambda|Omega)\b"
    r"|\b(?:on|of|across|over|from|into|in)\s+\$\\mathbb\{(?!R\})[A-Z]\}"
)

TRIVIAL_NUMERIC_RE = re.compile(r"[+-]?\d+(?:\.\d+)?")
TRIVIAL_IDENTIFIER_RE = re.compile(r"[A-Za-z][A-Za-z0-9']*")
TRIVIAL_LATEX_ATOM_RE = re.compile(r"\\(?:mathbf|boldsymbol|mathbb|mathrm)\{[A-Za-z0-9]+\}")
TRIVIAL_ASYMPTOTIC_PREFIXES = (r"\mathcal{O}", r"\Theta", r"\Omega", r"\mathcal{o}")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _build_acronym_re(config: LintConfig) -> re.Pattern[str]:
    """Build the acronym regex, including any project-specific additions."""
    base_acronyms = ["IVT", "WTA"]
    all_acronyms = base_acronyms + config.extra_acronyms
    pattern = r"\b(?:" + "|".join(re.escape(a) for a in all_acronyms) + r")\b"
    return re.compile(pattern)


def _build_banned_transition_re(config: LintConfig) -> re.Pattern[str]:
    """Build the banned-transition regex, including any project-specific additions."""
    base = (
        r"equivalently|more explicitly|this gives|rewriting|note that|notice that|recall that|observe that|"
        r"clearly|obviously|naturally|of course|straightforward(?:ly)?|it can be shown|it is easy to see|it follows that"
    )
    if config.extra_banned_transitions:
        extras = "|".join(re.escape(t) for t in config.extra_banned_transitions)
        combined = base + "|" + extras
    else:
        combined = base
    return re.compile(
        r"^\s*(?:>\s*)*(?:(?:[-*+])\s+|\d+\.\s+)?(?:" + combined + r")\b",
        re.IGNORECASE,
    )


def has_binary_minus(text: str) -> bool:
    for i, ch in enumerate(text):
        if ch != "-":
            continue
        j = i - 1
        while j >= 0 and text[j].isspace():
            j -= 1
        prev = text[j] if j >= 0 else None
        if prev is None or prev in {"(", "[", "{", ",", "^", "_"}:
            continue
        return True
    return False


def _is_simple_inline_expr(expr: str) -> bool:
    if len(expr) > 60:
        return False
    if "\\frac" in expr or "\\sum" in expr or "\\int" in expr:
        return False
    if "+" in expr:
        return False
    if has_binary_minus(expr):
        return False
    if not re.fullmatch(r"[A-Za-z0-9\\_^{}()\[\]|,.'\s:/+-]+", expr):
        return False
    return True


def is_trivial_inline_equality(content: str) -> bool:
    content_stripped = content.strip()
    eq_count = content_stripped.count("=")
    if eq_count == 0:
        return False

    if eq_count >= 2 and ":=" not in content_stripped:
        parts = [p.strip() for p in content_stripped.split("=")]
        if all(parts) and all(_is_simple_inline_expr(p) for p in parts):
            return True

    if eq_count != 1:
        return False

    if ":=" in content_stripped:
        left, right = (part.strip() for part in content_stripped.split(":=", 1))
    else:
        left, right = (part.strip() for part in content_stripped.split("=", 1))
    if not left or not right:
        return False

    rhs_is_numeric = bool(TRIVIAL_NUMERIC_RE.fullmatch(right))
    rhs_is_identifier = bool(TRIVIAL_IDENTIFIER_RE.fullmatch(right))
    rhs_is_latex_atom = bool(TRIVIAL_LATEX_ATOM_RE.fullmatch(right))
    rhs_is_asymptotic = right.lstrip().startswith(TRIVIAL_ASYMPTOTIC_PREFIXES)

    if rhs_is_numeric or rhs_is_identifier or rhs_is_latex_atom:
        return _is_simple_inline_expr(left)

    if rhs_is_asymptotic:
        return _is_simple_inline_expr(left) and _is_simple_inline_expr(right)

    return _is_simple_inline_expr(left) and _is_simple_inline_expr(right)


def iter_markdown_files(
    paths: list[Path], *, include_archives: bool, archive_dirs: set[str]
) -> Iterator[Path]:
    for path in paths:
        if path.is_dir():
            for candidate in (p for p in path.rglob("*.md") if p.is_file()):
                if not include_archives and any(
                    part in archive_dirs for part in candidate.parts
                ):
                    continue
                yield candidate
        else:
            yield path


def previous_nonempty_noncode_line(
    lines: list[str], start_index: int
) -> tuple[int, str] | None:
    for j in range(start_index - 1, -1, -1):
        text = lines[j].strip()
        if not text:
            continue
        return j + 1, lines[j]
    return None


def ends_with_punctuation(text: str) -> bool:
    stripped = text.rstrip()
    return bool(stripped) and stripped[-1] in {".", ",", ";", ":"}


def _strip_callout_and_list_prefix(text: str) -> str:
    probe = text.strip()
    while probe.startswith(">"):
        probe = probe[1:].lstrip()
    probe = re.sub(r"^(?:[-*+]|\d+\.)\s+", "", probe)
    return probe.strip()


# ---------------------------------------------------------------------------
# Core linting
# ---------------------------------------------------------------------------

def lint_file(path: Path, config: LintConfig | None = None) -> list[Issue]:
    """Lint a single Markdown file and return a list of issues.

    Parameters
    ----------
    path : Path
        Path to the Markdown file.
    config : LintConfig or None
        Override configuration. If None, all default rules are active.
    """
    if config is None:
        config = LintConfig()

    disabled = config.disabled_rules
    acronym_re = _build_acronym_re(config)
    banned_transition_re = _build_banned_transition_re(config)

    try:
        text = path.read_text(encoding="utf-8")
    except Exception as exc:
        return [Issue(path, 1, "io", f"Could not read file: {exc}")]

    lines = text.splitlines()
    issues: list[Issue] = []

    in_code_fence = False
    code_fence_token: str | None = None

    in_display = False
    display_start_line: int | None = None
    last_math_content_line: str | None = None
    last_math_content_lineno: int | None = None

    def check_display_leadin(open_lineno: int, open_index: int) -> None:
        if "display_leadin" in disabled:
            return
        prev = previous_nonempty_noncode_line(lines, open_index)
        if prev is None:
            issues.append(Issue(path, open_lineno, "display_leadin", "Display math has no preceding explanatory line."))
            return
        prev_lineno, prev_line = prev
        prev_stripped = prev_line.strip()
        if prev_stripped == "$$":
            issues.append(Issue(path, open_lineno, "display_leadin", "Display math follows another $$ line; add an explanatory sentence."))
        if HEADING_RE.match(prev_stripped):
            issues.append(Issue(path, open_lineno, "display_leadin", "Display math starts directly after a heading; add an explanatory sentence."))
        prev_probe = _strip_callout_and_list_prefix(prev_line)
        if CONTENT_FREE_LEADIN_RE.fullmatch(prev_probe):
            issues.append(
                Issue(path, open_lineno, "display_leadin",
                      "Display math is preceded by a content-free lead-in; name the operation or role of the equation.")
            )

    def close_display(close_lineno: int) -> None:
        nonlocal in_display, display_start_line, last_math_content_line, last_math_content_lineno
        in_display = False
        if "display_punctuation" not in disabled:
            if last_math_content_line is not None and last_math_content_lineno is not None:
                if ends_with_punctuation(last_math_content_line):
                    issues.append(
                        Issue(path, last_math_content_lineno, "display_punctuation",
                              "Trailing punctuation inside display math block; remove punctuation before closing $$.")
                    )
        display_start_line = None
        last_math_content_line = None
        last_math_content_lineno = None

    proof_open = False
    for i, line in enumerate(lines):
        lineno = i + 1
        stripped = line.strip()
        line_for_checks = INLINE_CODE_RE.sub("", line)
        table_probe = line_for_checks.lstrip()
        is_callout_line = table_probe.startswith(">")
        while table_probe.startswith(">"):
            table_probe = table_probe[1:].lstrip()
        is_table_row = table_probe.startswith("|")
        is_list_item = bool(re.match(r"^\s*(?:>\s*)*(?:[-*+]|\d+\.)\s+", line_for_checks))
        is_structured_context = is_table_row or is_callout_line or is_list_item

        fence_match = FENCE_RE.match(stripped)
        if fence_match:
            token = fence_match.group(1)
            if not in_code_fence:
                in_code_fence = True
                code_fence_token = token
            else:
                if code_fence_token == token:
                    in_code_fence = False
                    code_fence_token = None
            continue

        if in_code_fence:
            continue

        # Display math delimiters
        if "$$" in line_for_checks:
            parts = line_for_checks.split("$$")
            delim_count = len(parts) - 1

            if delim_count >= 3:
                issues.append(Issue(path, lineno, "display_ambiguous", "Ambiguous use of multiple $$ delimiters on one line."))

            if not in_display:
                check_display_leadin(lineno, i)
                in_display = True
                display_start_line = lineno

                if delim_count >= 2:
                    content = parts[1].strip()
                    if ends_with_punctuation(content):
                        issues.append(
                            Issue(path, lineno, "display_punctuation",
                                  "Trailing punctuation inside $$...$$; remove punctuation before closing $$.")
                        )
                    close_display(lineno)
                    continue

                remainder = parts[1] if len(parts) > 1 else ""
                if remainder.strip():
                    last_math_content_line = remainder
                    last_math_content_lineno = lineno
                continue

            before_close = parts[0]
            if before_close.strip():
                last_math_content_line = before_close
                last_math_content_lineno = lineno
            close_display(lineno)
            continue

        if in_display:
            if stripped:
                last_math_content_line = line
                last_math_content_lineno = lineno
                if "shorthand" not in disabled and RHO_INPUT_MAG_RE.search(line):
                    issues.append(
                        Issue(path, lineno, "shorthand",
                              "Avoid introducing shorthand for the input magnitude unless it materially improves clarity.")
                    )
            continue

        # Inline math checks
        if "inline_math" not in disabled and not is_structured_context:
            for match in INLINE_MATH_RE.finditer(line_for_checks):
                content = match.group(1)
                content_stripped = content.strip()
                has_eq = "=" in content_stripped
                if has_eq and is_trivial_inline_equality(content_stripped):
                    continue
                if has_eq or "\\frac" in content_stripped or len(content_stripped) > 40:
                    issues.append(
                        Issue(path, lineno, "inline_math",
                              "Inline math looks equation-like; prefer a preceding sentence and a $$...$$ block.")
                    )
                    break

        # Cross-link checks
        if "heading_link" not in disabled:
            for _ in HEADING_LINK_RE.finditer(line_for_checks):
                issues.append(
                    Issue(path, lineno, "heading_link",
                          "Link uses a heading-slug fragment; use a block anchor (^...) instead.")
                )

        # Imperative openings
        if "imperative" not in disabled:
            imperative_match = IMPERATIVE_START_RE.match(line_for_checks)
            if imperative_match:
                verb = imperative_match.group(1)
                issues.append(
                    Issue(path, lineno, "imperative",
                          f"Avoid imperative '{verb} ...' at the start of a line; rephrase declaratively.")
                )

        no_inline_math_simple = INLINE_MATH_RE.sub("", line_for_checks)

        # Banned transitions
        if "banned_transition" not in disabled:
            if banned_transition_re.match(no_inline_math_simple):
                issues.append(
                    Issue(path, lineno, "banned_transition",
                          "Banned transition lead-in detected; name the operation or state the claim directly.")
                )

        prose_probe = no_inline_math_simple

        # First person
        if "first_person" not in disabled:
            if LET_US_RE.search(prose_probe) or FIRST_PERSON_RE.search(prose_probe):
                issues.append(Issue(path, lineno, "first_person", "First-person phrasing detected; rewrite impersonally."))
            if GENERIC_ONE_RE.search(prose_probe):
                issues.append(Issue(path, lineno, "first_person", "Generic 'one can ...' phrasing detected; rewrite impersonally."))

        # Contractions
        if "contractions" not in disabled:
            if CONTRACTION_RE.search(prose_probe):
                issues.append(Issue(path, lineno, "contractions", "Contraction detected; use the full form."))

        # Vague phrasing
        if "vague_phrasing" not in disabled:
            if IN_WAYS_RE.search(prose_probe):
                issues.append(Issue(path, lineno, "vague_phrasing", "Vague phrase 'in ... ways' detected; state the mechanism."))

        # See link scaffolding
        if "see_link" not in disabled:
            if SEE_LINK_RE.search(no_inline_math_simple):
                issues.append(
                    Issue(path, lineno, "see_link",
                          "Avoid 'See [link]' scaffolding; integrate the reference inline with descriptive anchor text.")
                )

        # Case scaffolding
        if "case_scaffolding" not in disabled:
            if IN_THE_CASE_START_RE.match(line_for_checks):
                issues.append(
                    Issue(path, lineno, "case_scaffolding",
                          "Avoid 'In the ... case ...' scaffolding; prefer 'For ...' or 'With ...'.")
                )
            if THE_CASE_NP_RE.search(no_inline_math_simple):
                issues.append(
                    Issue(path, lineno, "case_scaffolding",
                          "Avoid 'the ... case' as a noun phrase; use the prepositional form.")
                )

        # Abstract framing
        if "abstract_framing" not in disabled:
            if ROLE_OF_RE.search(no_inline_math_simple):
                issues.append(
                    Issue(path, lineno, "abstract_framing",
                          "Abstract framing: 'the role of X in ...' detected; rewrite so X is the subject.")
                )
            if NATURE_OF_RE.search(no_inline_math_simple):
                issues.append(
                    Issue(path, lineno, "abstract_framing",
                          "Abstract framing: 'the nature of the ...' detected; delete or rewrite with the direct property.")
                )
            if TREATMENT_OF_RE.search(no_inline_math_simple):
                issues.append(
                    Issue(path, lineno, "abstract_framing",
                          "Nominalization: 'treatment(s) of' detected; prefer 'theory for' or the direct verb.")
                )

        # Acronyms
        if "acronyms" not in disabled:
            if acronym_re.search(no_inline_math_simple):
                issues.append(
                    Issue(path, lineno, "acronyms",
                          "Acronym detected; prefer the full name, optionally introducing the acronym once in parentheses.")
                )

        # Shorthand
        if "shorthand" not in disabled:
            if RHO_INPUT_MAG_RE.search(line_for_checks):
                issues.append(
                    Issue(path, lineno, "shorthand",
                          "Avoid introducing shorthand for the input magnitude unless it materially improves clarity.")
                )

        # Numbered case splits
        if "numbered_case" not in disabled:
            if NUMBERED_CASE_RE.search(line_for_checks):
                issues.append(Issue(path, lineno, "numbered_case", "Numbered case split detected; use named cases with semantic labels."))

        # Raw anchor tokens in running text
        if "raw_anchor" not in disabled:
            no_link_dest = LINK_DEST_RE.sub("]()", line_for_checks)
            no_inline_math = INLINE_MATH_RE.sub("", no_link_dest)
            for match in ANCHOR_TOKEN_RE.finditer(no_inline_math):
                if no_inline_math[match.end():].strip() == "":
                    continue
                issues.append(
                    Issue(path, lineno, "raw_anchor",
                          "Raw block anchor token used in running text; reference anchors via Markdown links.")
                )
                break

        # Bare symbols
        if "bare_symbol" not in disabled:
            if BARE_SYMBOL_RE.search(line_for_checks):
                issues.append(
                    Issue(path, lineno, "bare_symbol",
                          "Bare symbol after quantifier/preposition; name the object before the symbol.")
                )
            if BARE_PREP_SYMBOL_RE.search(line_for_checks):
                issues.append(
                    Issue(path, lineno, "bare_symbol",
                          "Bare symbol after preposition; name the object before the symbol.")
                )
            bare_space_match = BARE_SPACE_SYMBOL_RE.search(line_for_checks)
            if bare_space_match:
                match_start = bare_space_match.start()
                preceding_text = line_for_checks[:match_start]
                bare_symbol_text = bare_space_match.group()
                dollar_idx = bare_symbol_text.index("$")
                symbol_fragment = bare_symbol_text[dollar_idx:]
                named_earlier = bool(
                    re.search(r"\w\s+" + re.escape(symbol_fragment), preceding_text)
                )
                if not named_earlier:
                    issues.append(
                        Issue(path, lineno, "bare_symbol",
                              "Bare space/set symbol after preposition; name the space before the symbol.")
                    )

        # Prose math paraphrases
        if "prose_math" not in disabled and "$" in line_for_checks:
            if TIMES_WORD_RE.search(line_for_checks) or MULTIPLIED_BY_RE.search(line_for_checks):
                issues.append(
                    Issue(path, lineno, "prose_math",
                          "Avoid 'times'/'multiplied by' to paraphrase multiplication; prefer an explicit product in math.")
                )
            if GIVEN_BY_RE.search(line_for_checks):
                issues.append(
                    Issue(path, lineno, "prose_math",
                          "Avoid replacing trivial equalities with 'given by' prose; prefer an explicit equality.")
                )
            if FIXED_TO_RE.search(line_for_checks):
                issues.append(
                    Issue(path, lineno, "prose_math",
                          "Avoid 'fixed to' prose for trivial constraints; prefer an explicit equality.")
                )
            if OF_ORDER_RE.search(line_for_checks):
                issues.append(
                    Issue(path, lineno, "prose_math",
                          "Avoid 'of order ...' paraphrase; prefer explicit Landau notation.")
                )

        if "prose_math" not in disabled:
            if CONVERGES_TO_ONE_RE.search(line_for_checks):
                issues.append(Issue(path, lineno, "prose_math", "Phrase 'converges to one' detected; prefer an explicit limit in math."))
            if INLINE_MATH_IS_ZERO_RE.search(line_for_checks):
                issues.append(Issue(path, lineno, "prose_math", "Inline-math '... is zero' detected; prefer an explicit equality."))

        # Generic link text
        if "generic_link_text" not in disabled:
            if GENERIC_LINK_TEXT_RE.search(line_for_checks):
                issues.append(
                    Issue(path, lineno, "generic_link_text",
                          "Avoid generic link text like '[Lemma (...)]'; use descriptive anchor text.")
                )

        # Proof markers
        probe = line_for_checks.strip()
        while probe.startswith(">"):
            probe = probe[1:].lstrip()
        if PROOF_MARKER_RE.search(probe):
            proof_open = True
        if "proof_marker" not in disabled and SQUARE_RE.search(probe):
            if not proof_open:
                issues.append(Issue(path, lineno, "proof_marker", "End-of-proof symbol without a preceding '*Proof.*' marker."))
            proof_open = False

    if in_display:
        issues.append(Issue(path, display_start_line or len(lines), "display_unclosed", "Unclosed display math block; missing closing $$."))

    return issues


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main(argv: list[str], config: LintConfig | None = None, domain: str = "math") -> int:
    """Main entry point for style linting."""
    parser = argparse.ArgumentParser(description="Lint math style in Markdown notes.")
    parser.add_argument(
        "--include-archives",
        action="store_true",
        help="Include Markdown files under archive directories when linting.",
    )
    parser.add_argument("paths", nargs="+", help="Markdown files or directories to lint.")
    args = parser.parse_args(argv)

    if config is None:
        config = LintConfig(domain=domain)

    input_paths = [Path(p) for p in args.paths]
    files = list(
        iter_markdown_files(input_paths, include_archives=args.include_archives, archive_dirs=config.archive_dirs)
    )
    if not files:
        print("No markdown files found.", file=sys.stderr)
        return 2

    all_issues: list[Issue] = []
    for path in files:
        if path.suffix != ".md":
            continue
        all_issues.extend(lint_file(path, config=config))

    if not all_issues:
        return 0

    for issue in sorted(all_issues, key=lambda x: (str(x.path), x.line, x.message)):
        print(f"{issue.path}:{issue.line}: [{issue.rule}] {issue.message}")

    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
