"""Shared option parsing helpers for structure rules."""

from __future__ import annotations

from collections.abc import Mapping

from hermeneia.document.model import BlockKind


def as_block_kind_name_tuple(
    raw: object, *, field: str
) -> tuple[str, ...] | None:
    """Validate and normalize block-kind option values."""

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
    """Resolve configured block-kind names to domain enums."""

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
    """Validate that options payload is a mapping with known keys only."""

    if not isinstance(raw, Mapping):
        raise ValueError("options must be a mapping")
    unknown = sorted(key for key in raw if key not in allowed)
    if unknown:
        raise ValueError(
            f"{scope} has unknown option keys: {', '.join(unknown)}"
        )
    return raw


def parse_block_kind_name(value: str, *, field: str) -> BlockKind:
    normalized = value.strip().lower()
    try:
        return BlockKind(normalized)
    except ValueError as exc:
        expected = ", ".join(sorted(kind.value for kind in BlockKind))
        raise ValueError(
            f"{field} includes unknown block kind '{value}'. "
            f"Expected one of: {expected}"
        ) from exc
