"""Application-facing parser contracts."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from hermeneia.document.model import Document


@dataclass(frozen=True)
class ParseRequest:
    """Parserequest."""

    source: str
    path: Path | None = None


class DocumentParser(Protocol):
    """Documentparser."""

    def parse(self, request: ParseRequest) -> Document: ...
