"""Rule checking the form of each prose string of a structured source against its kind."""

from __future__ import annotations

import re

from hermeneia.document.model import FieldKind, FieldString, Sentence
from hermeneia.rules.base import AnnotatedRule, Layer, Severity
from hermeneia.rules.clauses import (
    SUBJECTS,
    children,
    clause_metadata,
    finding,
    prose_sentences,
    root,
)

#: A value written as the uppercase description of the content expected in a template.
PLACEHOLDER_RE = re.compile(r"^[A-Z][A-Z0-9 ,;/()_-]*[A-Z]$")
#: A sentence ending, followed by a new capitalized sentence.
SENTENCE_RESTART_RE = re.compile(r"[.!?]\s+[A-Z]")
#: Punctuation closing a sentence.
CLOSING = (".", "!", "?")


class FieldFormRule(AnnotatedRule):
    """Check each string of a structured source against the form fixed by its kind.

    A comment is a terse lowercase qualifier without a final period. A label closes without a
    period. A gloss is a noun phrase or a clause without a subject, opening in lowercase and
    closing without a period. A paragraph holds sentences with a subject and a finite verb, opening
    on a capital and closing on a period. A template value stays empty, its description standing in the
    comment of its line.
    """

    metadata = clause_metadata(
        "structure.field_form",
        "Prose string of a structured source takes the form of its kind",
        severity=Severity.WARNING,
        layer=Layer.SURFACE_STYLE,
    )

    def check(self, doc, ctx):
        """Report each string breaking the form of its kind.

        Parameters
        ----------
        doc : Document
            Document instance to inspect, carrying the strings of its source.
        ctx : RuleContext
            Rule evaluation context.

        Returns
        -------
        list[Violation]
            One violation per string breaking its form.
        """
        _ = ctx
        if not doc.fields:
            return []
        forms = _declared_forms(self.settings.options.get("forms"))
        sentences = [sentence for _block, _position, sentence in prose_sentences(doc)]
        violations = []
        fields = sorted(doc.fields, key=lambda item: item.line)
        for index, item in enumerate(fields):
            last = fields[index + 1].line - 1 if index + 1 < len(fields) else None
            own = [
                s
                for s in sentences
                if s.span.start_line >= item.line and (last is None or s.span.start_line <= last)
            ]
            declared = forms.get(item.key) if item.key is not None else None
            problem = (
                _problem(item, own) if declared is None else _declared_problem(declared, item, own)
            )
            if problem is None or not own:
                continue
            check, message = problem
            violations.append(
                finding(
                    self,
                    own[0].span,
                    message,
                    check,
                    "Rewrite the string in the form of its kind.",
                    confidence=0.7,
                )
            )
        return violations


#: Forms declarable by a project for the values of a key.
DECLARABLE_FORMS = frozenset({"gloss", "paragraph", "label"})


def _declared_forms(raw: object) -> dict[str, str]:
    """Return the form declared for each key, read from the option ``forms``.

    Raises
    ------
    ValueError
        If the option is not a mapping of keys to declarable forms.

    Examples
    --------
    >>> _declared_forms({"purpose": "gloss"})
    {'purpose': 'gloss'}
    """
    if raw is None:
        return {}
    if not isinstance(raw, dict) or any(form not in DECLARABLE_FORMS for form in raw.values()):
        raise ValueError(
            "structure.field_form option 'forms' maps each key to one of: "
            + ", ".join(sorted(DECLARABLE_FORMS))
        )
    return {str(key): str(form) for key, form in raw.items()}


def _declared_problem(
    form: str, item: FieldString, sentences: list[Sentence] | None = None
) -> tuple[str, str] | None:
    """Return the check failed by a string against the form declared for its key.

    A declared form outranks the form read from the construction of the string, as a project may
    write a clause with a subject as an entry, opening in lowercase.

    Examples
    --------
    >>> from hermeneia.document.model import FieldKind, FieldString
    >>> _declared_problem("gloss", FieldString(FieldKind.VALUE, "purpose", "the gain decays.", 1, 1))[0]
    'gloss_period'
    >>> _declared_problem("paragraph", FieldString(FieldKind.VALUE, "note", "The gain decays.", 1, 1)) is None
    True
    """
    text = item.text.strip().strip("\"'")
    if not text:
        return None
    if form == "label":
        return (
            ("label_period", "A label closes without a final period.")
            if text.endswith(".")
            else None
        )
    if form == "paragraph":
        if not text[0].isupper():
            return (
                "paragraph_lowercase",
                f"The key '{item.key}' holds sentences: open the value on a capital.",
            )
        if not text.endswith(CLOSING):
            return (
                "paragraph_period",
                f"The key '{item.key}' holds sentences: close the value on a period.",
            )
        return None
    if _opens_on_capital(text, sentences or []):
        return "gloss_capital", f"The key '{item.key}' holds an entry: open the value in lowercase."
    if text.endswith(CLOSING):
        return (
            "gloss_period",
            f"The key '{item.key}' holds an entry: close the value without a period.",
        )
    return None


def _problem(item: FieldString, sentences: list[Sentence]) -> tuple[str, str] | None:
    """Return the check failed by a string and its message, or None when its form holds."""
    text = item.text.strip().strip("\"'")
    if not text:
        return None
    if item.kind == FieldKind.COMMENT:
        if _opens_on_capital(text, sentences):
            return (
                "comment_capital",
                "A comment is a terse lowercase qualifier: open it in lowercase.",
            )
        if text.endswith(CLOSING):
            return "comment_period", "A comment closes without a final period."
        return None
    if item.kind in {FieldKind.LABEL, FieldKind.COMMIT_SUBJECT}:
        if text.endswith("."):
            return "label_period", "A label closes without a final period."
        return None
    if item.kind != FieldKind.VALUE:
        return None
    if PLACEHOLDER_RE.match(text) and len(text.split()) >= 2:
        return (
            "template_placeholder",
            "A template value stays empty: move the description of the content into the comment of its line.",
        )
    if _holds_sentence(sentences):
        if not text[0].isupper():
            return "paragraph_lowercase", "A value holding sentences opens on a capital."
        if not text.endswith(CLOSING):
            return "paragraph_period", "A value holding sentences closes on a period."
        return None
    if text[0].islower() and SENTENCE_RESTART_RE.search(text):
        return (
            "mixed_forms",
            "A gloss continued by a capitalized sentence mixes two forms: choose one.",
        )
    if _opens_on_capital(text, sentences):
        return "gloss_capital", "A gloss opens in lowercase, as a dictionary entry does."
    if text.endswith("."):
        return "gloss_period", "A gloss closes without a final period."
    return None


def _holds_sentence(sentences: list[Sentence]) -> bool:
    """Whether a string holds a sentence: a root verb carrying a subject.

    A gloss may hold a verb inside a relative or participial clause, as in "the target of a link,
    whose text stays scanned", whereas its root stays a noun.
    """
    for sentence in sentences:
        tokens = sentence.tokens
        main = root(tokens)
        if main is None or tokens[main].pos not in {"VERB", "AUX"}:
            continue
        if any(tokens[i].dep in SUBJECTS for i in children(tokens, main)):
            return True
    return False


def _opens_on_capital(text: str, sentences: list[Sentence]) -> bool:
    """Whether a string opens on a capital that is neither an acronym nor a proper noun."""
    if not text[0].isupper() or (len(text) > 1 and text[1].isupper()):
        return False
    first = next((t for s in sentences for t in s.tokens if t.text[:1].isalpha()), None)
    return first is None or first.pos != "PROPN"


def register(registry) -> None:
    """Register.

    Parameters
    ----------
    registry : object
        Rule registry used to resolve implementations.
    """
    registry.add(FieldFormRule)
