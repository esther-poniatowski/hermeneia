# Usage

This guide presents the operational flow from first run to policy tuning.

> [!NOTE]
> Hermeneia reports findings as diagnostics linked to likely reader-comprehension cost and does not auto-rewrite source files by default.

## Run Lint

### Quick Check

Start by verifying package and platform diagnostics:

```sh
hermeneia info
```

### Analyze One File

Start to lint one file to validate profile behavior:

```sh
hermeneia lint notes.md --profile research
```

### Analyze a Directory

After the single-file check, run the same profile on a directory:

```sh
hermeneia lint docs/ --profile pedagogical
```

`lint` recursively collects `.md` and `.markdown` files and then supports rule-scope refinement with the filters below.

## Configure Rule Scope

### Filter Rules
To diagnose one writing dimension at a time, several filtering options are available.

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

### Use Project Configuration

Load project policy from YAML:

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

## Control Output and Exit Behavior

### Use JSON Output

To feed diagnostics to scripts or in continuous integration pipelines, use JSON output:

```sh
hermeneia lint notes.md --format json
```

### Control Exit Behavior

To enforce thresholds in automated checks, use `--fail-on` to specify the minimum severity that should cause a non-zero exit code:

```sh
hermeneia lint notes.md --fail-on warning
```

## Interpret Results

### Output Model

The linter emits several outputs:

- diagnostics (operational + rule execution issues)
- rule violations with evidence/confidence/rationale
- revision plan operations
- scoring output (when enabled by config)

Interpret these outputs before editing text so revisions follow severity and structure.

### Interpreting Diagnostics

Treat diagnostics in this order:

1. blocker violations and structural defects
2. discourse and paragraph continuity issues
3. surface-level style improvements

Evidence fields identify the detected pattern, confidence and rationale indicate how deterministic detection is, and heuristic signals should guide review rather than replace editorial judgment.

This interpretation order aligns with the audit contract in [Prose Audit Protocol](prose-audit-protocol.md).

### Readability Signals

Hermeneia can report readability-oriented supporting signals such as:

- words per sentence
- sentences per paragraph
- passive-voice frequency
- pronoun density
- Flesch-style readability metrics

These statistics help prioritize revisions.
However, they do not, on their own, prove argument quality or pedagogical clarity.

For complete command syntax, see [CLI Reference](cli-reference.md).
