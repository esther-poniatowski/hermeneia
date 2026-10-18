"""Lines changed in a git working tree, read from ``git diff``.

A run limited to the changed lines reports only the findings of the current edit. A tracked file
contributes the lines added or modified since a base revision, and an untracked file contributes
every line.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

#: Header of a hunk of a unified diff without context, giving the new range of lines.
HUNK_RE = re.compile(r"^@@ -\d+(?:,\d+)? \+(?P<start>\d+)(?:,(?P<count>\d+))? @@")


class ChangeError(RuntimeError):
    """Raised when git cannot report the changes of a target."""


def repository_root(path: Path) -> Path:
    """Return the root of the git repository holding a path.

    Raises
    ------
    ChangeError
        If the path lies outside a git repository.
    """
    directory = path if path.is_dir() else path.parent
    result = _git(directory, "rev-parse", "--show-toplevel")
    return Path(result.strip())


def changed_files(target: Path, base: str) -> tuple[Path, ...]:
    """Return the files under a target that differ from a base revision, untracked files included."""
    root = repository_root(target)
    names = set(
        _git(
            root, "diff", "--name-only", "--diff-filter=ACMR", base, "--", str(target)
        ).splitlines()
    )
    names |= set(
        _git(root, "ls-files", "--others", "--exclude-standard", "--", str(target)).splitlines()
    )
    return tuple(sorted(root / name for name in names if name and (root / name).is_file()))


def changed_lines(path: Path, base: str) -> frozenset[int] | None:
    """Return the lines of a file added or modified since a base revision.

    Returns
    -------
    frozenset[int] | None
        The one-based changed lines, or None when the file is untracked and every line is new.
    """
    root = repository_root(path)
    tracked = subprocess.run(
        ["git", "ls-files", "--error-unmatch", str(path)],
        cwd=root,
        capture_output=True,
        check=False,
    )
    if tracked.returncode != 0:
        return None
    return parse_hunks(_git(root, "diff", "-U0", base, "--", str(path)))


def parse_hunks(diff: str) -> frozenset[int]:
    """Return the new lines covered by the hunks of a unified diff.

    Examples
    --------
    >>> sorted(parse_hunks("@@ -3,0 +4,2 @@\\n+a\\n+b\\n@@ -9 +11 @@\\n-x\\n+y"))
    [4, 5, 11]
    >>> sorted(parse_hunks("@@ -5,2 +4,0 @@"))
    []
    """
    lines: set[int] = set()
    for line in diff.splitlines():
        match = HUNK_RE.match(line)
        if match is None:
            continue
        start = int(match["start"])
        count = int(match["count"]) if match["count"] is not None else 1
        lines.update(range(start, start + count))
    return frozenset(lines)


def _git(directory: Path, *args: str) -> str:
    """Run a git command in a directory and return its output."""
    result = subprocess.run(
        ["git", *args], cwd=directory, capture_output=True, text=True, check=False
    )
    if result.returncode != 0:
        raise ChangeError(result.stderr.strip() or f"git {' '.join(args)} failed")
    return result.stdout
