# Usage

## Quick Check

```sh
hermeneia info
```

`hermeneia info` prints package and platform diagnostics.

## Analyze One File

```sh
hermeneia lint notes.md --profile research
```

## Analyze a Directory

```sh
hermeneia lint docs/ --profile pedagogical
```

`lint` recursively collects `.md` and `.markdown` files.

## Filter Rules

```sh
hermeneia lint notes.md \
  --rule surface.contraction \
  --rule discourse.subject_verb_distance
```

Disable specific rules after profile resolution:

```sh
hermeneia lint notes.md --disable-rule surface.passive_voice
```

## Use JSON Output

```sh
hermeneia lint notes.md --format json
```

## Control Exit Behavior

Fail when warnings or errors are present:

```sh
hermeneia lint notes.md --fail-on warning
```

## Use Project Configuration

```sh
hermeneia lint notes.md --config hermeneia.yaml
```

See [Configuration](configuration.md) for schema and merge semantics.

## Load External Rule Modules

```sh
hermeneia lint notes.md --load-rules custom_rules.math_pack
```

External modules must expose `register(registry)`.

## Output Model

`lint` never edits source files. It emits:

- diagnostics (operational + rule execution issues)
- rule violations with evidence/confidence/rationale
- revision plan operations
- scoring output (when enabled by config)
