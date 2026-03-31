# Usage

Hermeneia diagnoses and improves technical, pedagogical, and mathematical
writing through profile-aware analysis. The tool applies stratified rule systems
at five levels of textual organization, from surface style to audience fit.

For the full command registry, refer to [CLI Reference](cli-reference.md). For
profile and rule selection, refer to [Configuration](configuration.md).

## Analyzing a Document

The `lint` command analyzes a document or directory and reports diagnostics:

```sh
hermeneia lint document.md
hermeneia lint docs/
```

## Selecting a Writing Profile

Profiles activate the rule subsets and severity levels appropriate to a genre.
The `--profile` flag selects among `research`, `pedagogical`, and `math`:

```sh
hermeneia lint notes/ --profile research
hermeneia lint lecture-notes/ --profile pedagogical
hermeneia lint proofs/ --profile math
```

The `math` profile enables hard blockers: nominalization, abstract framing,
bare pronouns after display equations, and bare symbols are treated as
mandatory violations.

## Filtering Rules

Restrict the analysis to specific rule groups or exclude individual rules:

```sh
hermeneia lint document.md --select surface,discourse
hermeneia lint document.md --ignore B3,B4
```

## Reviewing Hard Blockers

The `check` command exits with a non-zero code when hard blockers remain,
making it suitable for CI integration and pre-commit hooks:

```sh
hermeneia check document.md --profile math
```

## Programmatic API

The same analysis is accessible from Python:

```python
from hermeneia.api import analyze

diagnostics = analyze("document.md", profile="research")
for d in diagnostics:
    print(f"{d.rule}: {d.message}")
```

## Next Steps

- [CLI Reference](cli-reference.md) — Full command registry and options.
- [Configuration](configuration.md) — Profiles, rule selection, severity.
- [Writing Standards](../standards/writing-standards.md) — The style rules enforced.
- [Math Style Rules](../rules/math-style-hard-rules.md) — Hard blockers for
  mathematical writing.
