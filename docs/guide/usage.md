# Usage

Hermeneia is a writing diagnostic tool targeting research, pedagogical, and
mathematical prose. The core analysis engine (linting, profiles, rule checking)
is **not yet implemented**. The current release exposes only platform diagnostics.

## Checking the Installation

The `info` command prints version and platform diagnostics — useful for
verifying that hermeneia is installed correctly and for including in bug reports:

```sh
hermeneia info
```

The `--version` / `-v` flag prints the version string alone:

```sh
hermeneia --version
```

## Planned Features

The following capabilities are planned but not yet available:

- **Document analysis** — Lint prose files against stratified rule systems at
  five levels of textual organization (surface style, sentence structure,
  discourse, mathematical notation, audience fit).
- **Writing profiles** — Activate rule subsets and severity levels by genre
  (`research`, `pedagogical`, `math`).
- **Rule filtering** — Select or ignore specific rule groups on the command
  line.
- **Hard-blocker checking** — Exit with a non-zero code when mandatory
  violations remain, suitable for CI and pre-commit hooks.
- **Python API** — Access the same analysis programmatically.

## Related Pages

- [CLI Reference](cli-reference.md) — Command registry and global options.
- [Writing Standards](../standards/writing-standards.md) — Style rules the
  analysis engine will enforce.
- [Math Style Rules](../rules/math-style-hard-rules.md) — Hard blockers for
  mathematical writing.
