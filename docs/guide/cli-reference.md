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

Use `lint` to analyze one file or a directory tree. A Markdown file is analyzed as a document. A YAML file, a Python module or a commit message is analyzed through its prose strings, as described in the [configuration of the inputs](configuration.md).

```sh
hermeneia lint [OPTIONS] TARGET...
```

**Argument**:

- `TARGET...` (`PATH`, one or more, required): files or directories to analyze. The configuration is searched from the first target. A file given as a target is analyzed regardless of its kind. A directory yields its files of the kinds listed in `inputs.kinds`.

**Options**:

- `--profile TEXT` (default `research`): profile preset (`research`, `strict`, `pedagogical`, `math`).
- `--config PATH`: YAML configuration file. When absent, the nearest `.hermeneia.yaml` or `.hermeneia.yml` at or above the target is read.
- `--format TEXT`: output format (`text`, `json`, or `compact`). The `compact` format prints one finding per line as `path:line[:column]: severity rule_id: message`.
- `--rule TEXT` (repeatable): restrict active rules to explicit ids.
- `--disable-rule TEXT` (repeatable): disable selected rules after resolution.
- `--load-rules TEXT` (repeatable): import external rule modules exposing `register(registry)`.
- `--experimental`: enable experimental rules.
- `--fail-on [info|warning|error]` (default `error`): non-zero exit threshold.
- `--changed`: report only the findings on lines added or modified since `--base`. Every line of an untracked file counts as changed. For a directory target, only its changed and untracked files are analyzed.
- `--base TEXT` (default `HEAD`): revision compared by `--changed`.
- `--kind TEXT` (repeatable): source kinds collected from a directory (`markdown`, `yaml`, `python`, `commit`), overriding `inputs.kinds`.
- `--no-exclude`: collect the directories listed in `inputs.exclude_dirs`.

To keep policy reproducible across runs, provide `--config` or select a fixed `--profile`.

```sh
hermeneia lint --profile research paper.md
hermeneia lint --changed --format compact .
hermeneia lint --format compact .git/COMMIT_EDITMSG
```

**Exit Codes**:

- `0`: success; no violations at or above `--fail-on`, and no fatal runtime error.
- `1`: at least one violation at or above `--fail-on`.
- `2`: fatal runtime/configuration/initialization error.

For post-run audit interpretation and severity semantics, see [Prose Audit Protocol](prose-audit-protocol.md).
