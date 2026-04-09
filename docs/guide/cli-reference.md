# CLI Reference

This reference is the command grammar companion to [Usage](usage.md).
Accordingly, it provides exact flags and exit contracts after the workflow overview.

## Global Command

Use this root form to invoke subcommands and global flags.

```text
hermeneia [OPTIONS] COMMAND [ARGS]...
```

### Global Options

- `--version`, `-v`: show package version and exit.
- `--help`: show help.

## `info`

Use `info` to print version and platform diagnostics.
Therefore, run this command first when environment behavior is uncertain.

```text
hermeneia info
```

## `lint`

Use `lint` to analyze one Markdown file or a directory tree.
Accordingly, pair these options with [Configuration](configuration.md) when policy must be reproducible across runs.

```text
hermeneia lint [OPTIONS] TARGET
```

### Argument

- `TARGET` (`PATH`, required): file or directory to analyze.

### Options

- `--profile TEXT` (default `research`): profile preset.
- `--config PATH`: YAML configuration file.
- `--format TEXT`: output format (`text` or `json`).
- `--rule TEXT` (repeatable): restrict active rules to explicit ids.
- `--disable-rule TEXT` (repeatable): disable selected rules after resolution.
- `--load-rules TEXT` (repeatable): import external rule modules exposing `register(registry)`.
- `--experimental`: enable experimental rules.
- `--fail-on [info|warning|error]` (default `error`): non-zero exit threshold.

### Exit Codes

- `0`: success; no violations at or above `--fail-on`, and no fatal runtime error.
- `1`: at least one violation at or above `--fail-on`.
- `2`: fatal runtime/configuration/initialization error.

For audit interpretation and severity semantics after command execution, see [Prose Audit Protocol](prose-audit-protocol.md).
