# Usage

Hermeneia reports writing issues as reader-impact diagnostics.
Accordingly, it does not auto-rewrite source files by default.
Therefore, this page shows the operational flow from first run to policy tuning.

## Quick Check

Use this command to verify package and platform diagnostics:

```sh
hermeneia info
```

Then run `lint` on one file before scaling to directories.

## Analyze One File

Start with one file to validate profile behavior:

```sh
hermeneia lint notes.md --profile research
```

## Analyze a Directory

After the single-file check, run the same profile on a directory:

```sh
hermeneia lint docs/ --profile pedagogical
```

`lint` recursively collects `.md` and `.markdown` files and then supports rule-scope refinement with the filters below.

## Filter Rules

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

Use these switches when diagnosing one writing dimension at a time.

## Use JSON Output

Use JSON when diagnostics feed scripts or continuous integration:

```sh
hermeneia lint notes.md --format json
```

## Control Exit Behavior

Use `--fail-on` to enforce thresholds in automated checks:

```sh
hermeneia lint notes.md --fail-on warning
```

## Use Project Configuration

Load project policy from YAML:

```sh
hermeneia lint notes.md --config hermeneia.yaml
```

See [Configuration](configuration.md) for schema and merge semantics.

## Load External Rule Modules

Load external rule packs through explicit module registration:

```sh
hermeneia lint notes.md --load-rules custom_rules.math_pack
```

External modules must expose `register(registry)`.

This extension point keeps custom rules inside the same scoring and reporting pipeline.

## Output Model

- diagnostics (operational + rule execution issues)
- rule violations with evidence/confidence/rationale
- revision plan operations
- scoring output (when enabled by config)

Interpret these outputs before editing text so revisions follow severity and structure.

## Interpreting Diagnostics

Treat diagnostics in this order:

1. blocker violations and structural defects
2. discourse and paragraph continuity issues
3. surface-level style improvements

Evidence fields identify the detected pattern, confidence and rationale indicate how deterministic detection is, and heuristic signals should guide review rather than replace editorial judgment.

This interpretation order aligns with the audit contract in [Prose Audit Protocol](prose-audit-protocol.md).

## Readability Signals

Hermeneia can report readability-oriented supporting signals such as:

- words per sentence
- sentences per paragraph
- passive-voice frequency
- pronoun density
- Flesch-style readability metrics

These statistics help prioritize revisions.
However, they do not, on their own, prove argument quality or pedagogical clarity.

For complete command syntax, see [CLI Reference](cli-reference.md).
