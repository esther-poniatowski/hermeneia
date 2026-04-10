# CLI Reference

This reference defines command grammar, option contracts, and exit codes.
For run order and interpretation workflow, see [Usage](usage.md).
For policy semantics, see [Configuration](configuration.md).

## Global Command

Use this root form to invoke subcommands and global flags.

```sh
hermeneia [OPTIONS] COMMAND [ARGS]...
```

### Global Options

- `--version`, `-v`: show package version and exit.
- `--help`: show help.

## Getting Info

Use `info` to print version and platform diagnostics.

```sh
hermeneia info
```

Run this command first when environment behavior is uncertain.

## Linting

Use `lint` to analyze one Markdown file or a directory tree.

```sh
hermeneia lint [OPTIONS] TARGET
```

**Argument**:

- `TARGET` (`PATH`, required): file or directory to analyze.

**Options**:

- `--profile TEXT` (default `research`): profile preset.
- `--config PATH`: YAML configuration file.
- `--format TEXT`: output format (`text` or `json`).
- `--rule TEXT` (repeatable): restrict active rules to explicit ids.
- `--disable-rule TEXT` (repeatable): disable selected rules after resolution.
- `--load-rules TEXT` (repeatable): import external rule modules exposing `register(registry)`.
- `--experimental`: enable experimental rules.
- `--fail-on [info|warning|error]` (default `error`): non-zero exit threshold.

To keep policy reproducible across runs, provide `--config` or select a fixed `--profile`.

```sh
hermeneia lint --profile research paper.md
```

**Exit Codes**:

- `0`: success; no violations at or above `--fail-on`, and no fatal runtime error.
- `1`: at least one violation at or above `--fail-on`.
- `2`: fatal runtime/configuration/initialization error.

For post-run audit interpretation and severity semantics, see [Prose Audit Protocol](prose-audit-protocol.md).
