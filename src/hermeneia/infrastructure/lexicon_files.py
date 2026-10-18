"""Terms of a project, read from the files declaring them.

A project names its own quantities and objects with nouns shaped like process nouns, such as
"finding" or "violation", and the nominalization rule exempts the declared terms. Reading the terms
from the files declaring them, such as glossaries, keeps a single list of terms.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable

import yaml

from hermeneia.config.schema import TerminologyConfig


def load_terms(config: TerminologyConfig, base: Path) -> frozenset[str]:
    """Return the lowercase terms listed in a configuration and in its files.

    Parameters
    ----------
    config : TerminologyConfig
        Terminology block of the project configuration.
    base : Path
        Directory against which the globs of the files resolve.

    Returns
    -------
    frozenset[str]
        The terms, lowercased.
    """
    terms = {term.lower() for term in config.terms}
    for entry in config.files:
        for path in sorted(base.glob(entry.path)):
            data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
            terms.update(str(value).lower() for value in select(data, entry.select.split(".")))
    return frozenset(term for term in terms if term)


def select(data: Any, keys: list[str]) -> Iterable[Any]:
    """Yield the values reached by a dotted path, where ``*`` matches every key of a mapping.

    A list met along the path is traversed item by item, and a list at the end yields its items.

    Examples
    --------
    >>> sorted(select({"terms": {"a": {"label": "gain"}, "b": {"label": "drive"}}}, ["terms", "*", "label"]))
    ['drive', 'gain']
    >>> list(select({"terms": ["finding", "violation"]}, ["terms"]))
    ['finding', 'violation']
    """
    if isinstance(data, list):
        for item in data:
            yield from select(item, keys)
        return
    if not keys:
        yield data
        return
    head, rest = keys[0], keys[1:]
    if not isinstance(data, dict):
        return
    if head == "*":
        for value in data.values():
            yield from select(value, rest)
    elif head in data:
        yield from select(data[head], rest)
