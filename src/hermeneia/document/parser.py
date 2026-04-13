"""Application-facing parser contracts."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from hermeneia.document.model import Document


@dataclass(frozen=True)
class ParseRequest:
    """Input payload for parsing a single source document."""

    source: str
    path: Path | None = None


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
