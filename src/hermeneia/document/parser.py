"""Application-facing parser contracts."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from hermeneia.document.model import Document, FieldString, SourceKind


@dataclass(frozen=True)
class ParseRequest:
    """Input payload for parsing a single source document.

    A structured source arrives already projected to Markdown, with its field strings and the
    source line of each projected line.
    """

    source: str
    path: Path | None = None
    source_kind: SourceKind = SourceKind.MARKDOWN
    fields: tuple[FieldString, ...] = ()
    line_map: tuple[int, ...] = ()


class DocumentParser(Protocol):
    """Protocol for document parser implementations."""

    def parse(self, request: ParseRequest) -> Document:
        """Parse request.

        Parameters
        ----------
        request : ParseRequest
            Structured request object for this operation.

        Returns
        -------
        Document
            Resulting value produced by this call.
        """
