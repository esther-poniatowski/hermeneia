"""Projection of the prose strings of a structured source to a Markdown document.

A YAML file, a Python module or a commit message holds prose in its values, comments, docstrings
and message body. Each string is written as one paragraph of a Markdown projection, separated from
the next by a blank line, so that two strings on consecutive source lines never merge into one
sentence. The projection records the source line of each of its lines and the kind of each string.
The kind of a string fixes the form required of it.
"""

from __future__ import annotations

import ast
import io
import re
import tokenize
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from hermeneia.document.model import FieldKind, FieldString, SourceKind

#: Suffixes of the structured sources, by kind.
SUFFIXES = {
    ".yml": SourceKind.YAML,
    ".yaml": SourceKind.YAML,
    ".py": SourceKind.PYTHON,
    ".md": SourceKind.MARKDOWN,
    ".markdown": SourceKind.MARKDOWN,
}
#: File names of a commit message, as git and editors write it.
COMMIT_NAMES = frozenset({"COMMIT_EDITMSG", "MERGE_MSG", "TAG_EDITMSG"})
#: Keys of a YAML value read as a label: a short noun phrase without a final period.
LABEL_KEYS = frozenset({"name", "title", "label", "heading", "alias", "aliases"})
#: Numpydoc sections holding no prose, skipped whole.
SKIPPED_SECTIONS = frozenset({"examples", "see also", "references"})
#: Numpydoc sections whose entries open on a specification line followed by a description.
ENTRY_SECTIONS = frozenset(
    {
        "parameters",
        "other parameters",
        "returns",
        "yields",
        "receives",
        "raises",
        "warns",
        "attributes",
    }
)
#: A trailer of a commit message, such as "Co-Authored-By: …".
TRAILER_RE = re.compile(r"^[A-Z][\w-]*(?:-[\w-]+)*:\s")
#: A comment holding commented-out code or data rather than prose.
CODE_COMMENT_RE = re.compile(
    r"^(?:[\w.\[\]\"'-]+\s*[:=(]|[-*]\s+\w+:|[{\[(<]|!|noqa|type:|pragma|pylint:|fmt:)"
)
#: A string holding prose: at least three words, one of them alphabetic and longer than two letters.
WORDS_RE = re.compile(r"[A-Za-z]{3,}")


@dataclass
class Projection:
    """A structured source projected to Markdown.

    Parameters
    ----------
    markdown : str
        The projection, one paragraph per string.
    line_map : tuple[int, ...]
        Source line of each line of the projection.
    fields : tuple[FieldString, ...]
        The strings, with their kind and their lines.
    """

    markdown: str = ""
    line_map: tuple[int, ...] = ()
    fields: tuple[FieldString, ...] = ()


@dataclass
class _Builder:
    """Accumulate the paragraphs of a projection."""

    lines: list[str] = field(default_factory=list)
    line_map: list[int] = field(default_factory=list)
    fields: list[FieldString] = field(default_factory=list)

    def add(
        self, kind: FieldKind, key: str | None, text_lines: list[str], source_line: int
    ) -> None:
        """Append one string as a paragraph, after a blank separating line."""
        cleaned = [line.strip() for line in text_lines]
        while cleaned and not cleaned[-1]:
            cleaned.pop()
        if not cleaned or not _is_prose(" ".join(cleaned)):
            return
        if self.lines:
            self.lines.append("")
            self.line_map.append(source_line)
        start = len(self.lines) + 1
        for offset, text in enumerate(cleaned):
            self.lines.append(text)
            self.line_map.append(source_line + offset)
        self.fields.append(FieldString(kind, key, " ".join(cleaned), start, source_line))

    def build(self) -> Projection:
        """Return the projection."""
        markdown = "\n".join(self.lines) + ("\n" if self.lines else "")
        return Projection(markdown, tuple(self.line_map), tuple(self.fields))


def source_kind(path: Path) -> SourceKind | None:
    """Return the kind of a source file, or None for a file holding no analyzable prose.

    Examples
    --------
    >>> source_kind(Path("config/checks.yaml")).value
    'yaml'
    >>> source_kind(Path(".git/COMMIT_EDITMSG")).value
    'commit'
    >>> source_kind(Path("figure.png")) is None
    True
    """
    if path.name in COMMIT_NAMES or path.suffix == ".commit":
        return SourceKind.COMMIT
    return SUFFIXES.get(path.suffix.lower())


def project(kind: SourceKind, source: str) -> Projection:
    """Project the prose strings of a structured source to Markdown.

    Parameters
    ----------
    kind : SourceKind
        Kind of the source; a Markdown source is returned unchanged.
    source : str
        Text of the source.

    Returns
    -------
    Projection
        The projection, its line map and its strings.
    """
    if kind == SourceKind.MARKDOWN:
        return Projection(markdown=source)
    builder = _Builder()
    if kind == SourceKind.YAML:
        _project_yaml(source, builder)
    elif kind == SourceKind.PYTHON:
        _project_python(source, builder)
    else:
        _project_commit(source, builder)
    return builder.build()


def project_frontmatter(source: str, keys: frozenset[str]) -> Projection:
    """Project the values of selected keys of the YAML frontmatter of a Markdown document.

    The body of the document is analysed as Markdown. Its frontmatter holds data, except for the
    keys whose values a project writes as prose, such as a purpose. Those values are projected like
    the values of a YAML source, located on their lines of the document.

    Parameters
    ----------
    source : str
        Text of the Markdown document.
    keys : frozenset[str]
        Keys of the frontmatter holding prose.

    Returns
    -------
    Projection
        The projection of the selected values, empty when the document has no frontmatter.

    Examples
    --------
    >>> text = '---\\nrole: note\\npurpose: "fixes the settings read by the checkers"\\n---\\n# Note\\n'
    >>> [(f.key, f.source_line) for f in project_frontmatter(text, frozenset({"purpose"})).fields]
    [('purpose', 3)]
    """
    lines = source.splitlines()
    if not keys or not lines or lines[0].strip() != "---":
        return Projection()
    closing = next((i for i in range(1, len(lines)) if lines[i].strip() in {"---", "..."}), None)
    if closing is None:
        return Projection()
    builder = _Builder()
    _project_yaml("\n".join(lines[1:closing]), builder, keys=keys, offset=1)
    return builder.build()


def _is_prose(text: str) -> bool:
    """Whether a string reads as prose rather than as an identifier, a path or a number.

    Examples
    --------
    >>> _is_prose("the terms of a project")
    True
    >>> _is_prose("utils/schemas/index-types")
    False
    """
    if len(text.split()) < 3 or not WORDS_RE.search(text):
        return False
    return not re.fullmatch(r"\[[^\]]*\]\([^)]*\)", text.strip("\"' "))


def _project_yaml(
    source: str, builder: _Builder, keys: frozenset[str] | None = None, offset: int = 0
) -> None:
    """Project the comments and the string values of a YAML source, in source order.

    When ``keys`` is given, only the values held by those keys are projected, without comments.
    The ``offset`` shifts every line, for a YAML block embedded in a longer file.
    """
    entries: list[tuple[int, FieldKind, str | None, list[str]]] = []
    lines = source.splitlines() if keys is None else []
    block: list[str] = []
    block_start = 0
    for number, line in enumerate(lines, start=1):
        comment = _yaml_comment(line)
        full_line = comment is not None and line.lstrip().startswith("#")
        if block and (not full_line or not comment):
            entries.append((block_start, FieldKind.COMMENT, None, block))
            block = []
        if comment is None or not comment or CODE_COMMENT_RE.match(comment):
            continue
        if full_line:
            if not block:
                block_start = number
            block.append(comment)
        else:
            entries.append((number, FieldKind.COMMENT, None, [comment]))
    if block:
        entries.append((block_start, FieldKind.COMMENT, None, block))
    try:
        root = yaml.compose(source)
    except yaml.YAMLError:
        root = None
    if root is not None:
        for key, node in _yaml_scalars(root, None):
            if keys is not None and key not in keys:
                continue
            kind = FieldKind.LABEL if key in LABEL_KEYS else FieldKind.VALUE
            first = node.start_mark.line + 1
            if node.style in {"|", ">"}:
                text_lines = node.value.splitlines()
                first += 1
            else:
                text_lines = [node.value.replace("\n", " ")]
            entries.append((first, kind, key, text_lines))
    for number, kind, key, text_lines in sorted(entries, key=lambda entry: entry[0]):
        builder.add(kind, key, text_lines, number + offset)


def _yaml_comment(line: str) -> str | None:
    """Return the text of the comment of a YAML line, outside quoted strings.

    Examples
    --------
    >>> _yaml_comment("key: 'a # b'  # optional")
    'optional'
    >>> _yaml_comment("# Settings of the checkers.")
    'Settings of the checkers.'
    """
    quote: str | None = None
    for index, char in enumerate(line):
        if quote is not None:
            if char == quote:
                quote = None
        elif char in {"'", '"'}:
            quote = char
        elif char == "#" and (index == 0 or line[index - 1].isspace()):
            return line[index + 1 :].strip()
    return None


def _yaml_scalars(node: yaml.Node, key: str | None):
    """Yield each string scalar of a YAML tree with the key holding it."""
    if isinstance(node, yaml.MappingNode):
        for key_node, value_node in node.value:
            yield from _yaml_scalars(value_node, str(key_node.value))
    elif isinstance(node, yaml.SequenceNode):
        for item in node.value:
            yield from _yaml_scalars(item, key)
    elif isinstance(node, yaml.ScalarNode) and node.tag == "tag:yaml.org,2002:str":
        yield key, node


def _project_python(source: str, builder: _Builder) -> None:
    """Project the docstrings and the comments of a Python module, in source order."""
    entries: list[tuple[int, FieldKind, list[str]]] = []
    try:
        tree = ast.parse(source)
    except SyntaxError:
        tree = None
    if tree is not None:
        for node in ast.walk(tree):
            if not isinstance(
                node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)
            ):
                continue
            if not node.body or not isinstance(node.body[0], ast.Expr):
                continue
            value = node.body[0].value
            if isinstance(value, ast.Constant) and isinstance(value.value, str):
                for line, text_lines in _docstring_paragraphs(value.value, value.lineno):
                    entries.append((line, FieldKind.DOCSTRING, text_lines))
    try:
        tokens = list(tokenize.generate_tokens(io.StringIO(source).readline))
    except (tokenize.TokenError, IndentationError):
        tokens = []
    block: list[str] = []
    block_start = 0
    previous_line = -2
    for token in tokens:
        if token.type != tokenize.COMMENT:
            continue
        text = token.string.lstrip("#:").strip()
        line = token.start[0]
        if line == 1 and token.string.startswith("#!") or CODE_COMMENT_RE.match(text):
            continue
        if line != previous_line + 1 and block:
            entries.append((block_start, FieldKind.CODE_COMMENT, block))
            block = []
        if not block:
            block_start = line
        block.append(text)
        previous_line = line
    if block:
        entries.append((block_start, FieldKind.CODE_COMMENT, block))
    for line, kind, text_lines in sorted(entries, key=lambda entry: entry[0]):
        builder.add(kind, None, text_lines, line)


def _docstring_paragraphs(docstring: str, first_line: int) -> list[tuple[int, list[str]]]:
    """Return the prose paragraphs of a numpydoc docstring, each with its source line.

    Section headers, specification lines of entries, doctest lines and the skipped sections are
    left out, whereas the description of each entry is kept.

    Examples
    --------
    >>> text = "Read a file.\\n\\nParameters\\n----------\\npath : Path\\n    File to read.\\n"
    >>> [lines for _, lines in _docstring_paragraphs(text, 1)]
    [['Read a file.'], ['File to read.']]
    """
    lines = docstring.splitlines()
    paragraphs: list[tuple[int, list[str]]] = []
    current: list[str] = []
    current_start = 0
    section: str | None = None
    index = 0

    def flush() -> None:
        nonlocal current
        if current:
            paragraphs.append((current_start, current))
        current = []

    while index < len(lines):
        raw = lines[index]
        text = raw.strip()
        following = lines[index + 1].strip() if index + 1 < len(lines) else ""
        if following and set(following) == {"-"} and text:
            flush()
            section = text.lower()
            index += 2
            continue
        skip = (
            not text
            or text.startswith((">>>", "..."))
            or section in SKIPPED_SECTIONS
            or (section in ENTRY_SECTIONS and not raw.startswith((" ", "\t")))
        )
        if skip:
            flush()
        else:
            if not current:
                current_start = first_line + index
            current.append(text)
        index += 1
    flush()
    return paragraphs


def _project_commit(source: str, builder: _Builder) -> None:
    """Project the subject and the body paragraphs of a commit message."""
    lines = source.splitlines()
    content = [
        (number, line)
        for number, line in enumerate(lines, start=1)
        if not line.startswith("#") and not TRAILER_RE.match(line)
    ]
    if not content:
        return
    subject_line, subject = next(((n, l) for n, l in content if l.strip()), (0, ""))
    if subject:
        builder.add(FieldKind.COMMIT_SUBJECT, None, [subject], subject_line)
    paragraph: list[str] = []
    start = 0
    for number, line in content:
        if number == subject_line:
            continue
        if not line.strip():
            if paragraph:
                builder.add(FieldKind.COMMIT_BODY, None, paragraph, start)
            paragraph = []
            continue
        if not paragraph:
            start = number
        paragraph.append(line)
    if paragraph:
        builder.add(FieldKind.COMMIT_BODY, None, paragraph, start)
