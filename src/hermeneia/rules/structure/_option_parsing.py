"""Shared option parsing helpers for structure rules.

Functions
---------
as_block_kind_name_tuple
    Public API symbol.
resolve_block_kinds
    Public API symbol.
mapping_with_allowed_keys
    Public API symbol.
parse_block_kind_name
    Public API symbol.
"""

from __future__ import annotations

from collections.abc import Mapping

from hermeneia.document.model import BlockKind

COMMA_SEPARATOR = ", "


def as_block_kind_name_tuple(raw: object, *, field: str) -> tuple[str, ...] | None:
    """Validate and normalize block-kind option values.

    Parameters
    ----------
    raw : object
        Raw value before validation.
    field : str
        Input value for ``field``.

    Returns
    -------
    tuple[str, ...] | None
        Resulting value produced by this call.
    """

    if raw is None:
        return None
    if isinstance(raw, str):
        values = (raw,)
    elif isinstance(raw, (list, tuple)):
        if not all(isinstance(item, str) for item in raw):
            raise ValueError(f"{field} must be a string or sequence of strings")
        values = tuple(raw)
    else:
        raise ValueError(f"{field} must be a string or sequence of strings")

    normalized: list[str] = []
    for value in values:
        normalized.append(parse_block_kind_name(value, field=field).value)
    return tuple(dict.fromkeys(normalized))


def resolve_block_kinds(
    raw: object, *, field: str, default: tuple[BlockKind, ...]
) -> frozenset[BlockKind]:
    """Resolve configured block-kind names to domain enums.

    Parameters
    ----------
    raw : object
        Raw value before validation.
    field : str
        Input value for ``field``.
    default : tuple[BlockKind, ...]
        Input value for ``default``.

    Returns
    -------
    frozenset[BlockKind]
        Resulting value produced by this call.
    """

    if raw is None:
        return frozenset(default)
    if isinstance(raw, str):
        values = (raw,)
    elif isinstance(raw, (list, tuple)):
        values = tuple(raw)
    else:
        raise ValueError(f"{field} must be a string or sequence of strings")
    kinds = [parse_block_kind_name(str(value), field=field) for value in values]
    return frozenset(kinds)


def mapping_with_allowed_keys(
    raw: object, *, allowed: frozenset[str], scope: str
) -> Mapping[str, object]:
    """Validate that options payload is a mapping with known keys only.

    Parameters
    ----------
    raw : object
        Raw value before validation.
    allowed : frozenset[str]
        Input value for ``allowed``.
    scope : str
        Input value for ``scope``.

    Returns
    -------
    Mapping[str, object]
        Resulting value produced by this call.
    """

    if not isinstance(raw, Mapping):
        raise ValueError("options must be a mapping")
    unknown = sorted(key for key in raw if key not in allowed)
    if unknown:
        raise ValueError(
            f"{scope} has unknown option keys: {COMMA_SEPARATOR.join(unknown)}"
        )
    return raw


def parse_block_kind_name(value: str, *, field: str) -> BlockKind:
    """Parse block kind name.

    Parameters
    ----------
    value : str
        Input value for ``value``.
    field : str
        Input value for ``field``.

    Returns
    -------
    BlockKind
        Resulting value produced by this call.
    """
    normalized = value.strip().lower()
    try:
        return BlockKind(normalized)
    except ValueError as exc:
        expected = ", ".join(sorted(kind.value for kind in BlockKind))
        raise ValueError(
            f"{field} includes unknown block kind '{value}'. "
            f"Expected one of: {expected}"
        ) from exc
