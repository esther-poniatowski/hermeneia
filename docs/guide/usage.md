# Usage

This guide presents the operational flow from first run to interpretation.
It is task-oriented, while exact flag grammar is described in [CLI Reference](cli-reference.md).

> [!NOTE]
> Hermeneia reports findings as diagnostics linked to likely reader-comprehension cost and does not auto-rewrite source files by default.

## Workflow

Use this sequence:

1. Run a baseline lint pass.
2. Narrow rule scope or load a project policy.
3. Set output and failure behavior for local or CI runs.
4. Interpret findings in structural-to-local priority order.

## Baseline Run

### Check Environment

Verify package and platform diagnostics:

```sh
hermeneia info
```

### Analyze One File

Run one-file analysis to validate profile behavior:

```sh
hermeneia lint notes.md --profile research
```

### Analyze a Directory

Then apply the same profile to a directory:

```sh
hermeneia lint docs/ --profile pedagogical
```

`lint` recursively collects `.md` and `.markdown` files.

## Adjust Scope and Policy

### Filter Rules

Use explicit allowlists to isolate one writing dimension:

```sh
hermeneia lint notes.md \
  --rule surface.contraction \
  --rule discourse.subject_verb_distance
```

Disable specific rules after profile resolution:

```sh
hermeneia lint notes.md --disable-rule surface.passive_voice
```

### Load Project Configuration

Load resolved policy from YAML:

```sh
hermeneia lint notes.md --config hermeneia.yaml
```

See [Configuration](configuration.md) for schema and merge semantics.

### Load External Rule Modules

Load external rule packs through explicit module registration:

```sh
hermeneia lint notes.md --load-rules custom_rules.math_pack
```

External modules must expose `register(registry)`.
This extension point keeps custom rules inside the same scoring and reporting pipeline.

## Control Output and CI Exit

### Use JSON Output

Use JSON output for scripts and CI:

```sh
hermeneia lint notes.md --format json
```

### Control Exit Behavior

Use `--fail-on` to define the minimum severity that should produce a non-zero exit code:

```sh
hermeneia lint notes.md --fail-on warning
```

## Interpret Results

### Result Components

The linter emits:

- diagnostics (operational + rule execution issues)
- rule violations with evidence/confidence/rationale
- revision plan operations
- scoring output (when enabled by config)

Read these outputs before editing so revision order follows severity and structure.

### Prioritize Findings

Treat diagnostics in this order:

1. blocker violations and structural defects
2. discourse and paragraph continuity issues
3. surface-level style improvements

Evidence fields identify the detected pattern, confidence and rationale indicate how deterministic detection is, and heuristic signals should guide review rather than replace editorial judgment.

This interpretation order aligns with the audit contract in [Prose Audit Protocol](prose-audit-protocol.md).

### Use Metrics as Supporting Signals

Readability metrics help prioritize revisions, but they do not prove argument quality on their own.
For definitions, formulas, and interpretation limits, see [Metrics](metrics.md).

For complete command syntax, see [CLI Reference](cli-reference.md).
