"""Block rule recognizing display math delimited by ``$$`` lines.

CommonMark knows no display math, so a ``$$`` line written directly after a line of text continues
that paragraph. Instead, Obsidian and most Markdown renderers start a display block there. This rule
gives the parser the same reading: a line opening on ``$$`` interrupts a paragraph and starts a
block that ends on the next line closing on ``$$``.
"""

from __future__ import annotations

from markdown_it import MarkdownIt
from markdown_it.rules_block import StateBlock

#: Token type pushed for a closed display-math block.
MATH_BLOCK_TOKEN = "math_block"
#: Delimiter opening and closing a display-math block.
DELIMITER = "$$"


def display_math_rule(state: StateBlock, start_line: int, end_line: int, silent: bool) -> bool:
    """Consume a display-math block opening on a ``$$`` line.

    An unclosed block is left to the paragraph rule, so that the rules reporting an unclosed
    delimiter still read it from the source lines.

    Parameters
    ----------
    state : StateBlock
        Block state of the markdown-it parser.
    start_line : int
        Index of the line where the block may open.
    end_line : int
        Index of the line closing the current container.
    silent : bool
        Whether the parser only probes whether the rule applies.

    Returns
    -------
    bool
        Whether a display-math block opens on ``start_line``.
    """
    if state.sCount[start_line] - state.blkIndent >= 4:
        return False
    first = _line_text(state, start_line)
    if not first.startswith(DELIMITER):
        return False
    closing = _closing_line(state, start_line, end_line, first)
    if closing is None:
        return False
    if silent:
        return True
    token = state.push(MATH_BLOCK_TOKEN, "math", 0)
    token.block = True
    token.markup = DELIMITER
    token.map = [start_line, closing + 1]
    token.content = state.getLines(start_line, closing + 1, state.sCount[start_line], False)
    state.line = closing + 1
    return True


def enable_display_math(markdown: MarkdownIt) -> MarkdownIt:
    """Register the display-math rule before the paragraph rule, so that a ``$$`` line interrupts a paragraph.

    Parameters
    ----------
    markdown : MarkdownIt
        Parser to extend.

    Returns
    -------
    MarkdownIt
        The same parser, for chaining.
    """
    markdown.block.ruler.before(
        "paragraph",
        "display_math",
        display_math_rule,
        {"alt": ["paragraph", "reference", "blockquote", "list"]},
    )
    return markdown


def _line_text(state: StateBlock, line: int) -> str:
    """Return the text of a line inside the current container, without its indentation."""
    start = state.bMarks[line] + state.tShift[line]
    return state.src[start : state.eMarks[line]].strip()


def _closing_line(state: StateBlock, start_line: int, end_line: int, first: str) -> int | None:
    """Return the index of the line closing the block, or None when the block stays open.

    A first line holding both delimiters, ``$$ x $$``, closes the block on itself.
    """
    if len(first) > len(DELIMITER) and first.endswith(DELIMITER):
        return start_line
    line = start_line + 1
    while line < end_line:
        if state.sCount[line] < state.blkIndent:
            return None
        if _line_text(state, line).endswith(DELIMITER):
            return line
        line += 1
    return None
