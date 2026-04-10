# Hermeneia

[![Conda](https://img.shields.io/badge/conda-eresthanaconda--channel-blue)](docs/guide/installation.md)
[![Maintenance](https://img.shields.io/maintenance/yes/2026)]()
[![Last Commit](https://img.shields.io/github/last-commit/esther-poniatowski/hermeneia)](https://github.com/esther-poniatowski/hermeneia/commits/main)
[![Python](https://img.shields.io/badge/python-%E2%89%A53.12-blue)](https://www.python.org/)
[![License: GPL](https://img.shields.io/badge/License-GPL--3.0-yellow.svg)](https://opensource.org/licenses/GPL-3.0)

Audits technical prose for clarity.

---

## Table of Contents

- [Hermeneia](#hermeneia)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
    - [Motivation](#motivation)
    - [Advantages](#advantages)
  - [Features](#features)
  - [Quick Start](#quick-start)
    - [CLI](#cli)
    - [Application Programming Interface](#application-programming-interface)
  - [Documentation](#documentation)
  - [Contributing](#contributing)
  - [Acknowledgments](#acknowledgments)
    - [Authors](#authors)
  - [License](#license)

## Overview

### Motivation

Technical and mathematical writing loose efficiency when readers cannot identify the main claim and its
support quickly. Hermeneia helps writers diagnose clarity defects and prioritize revisions across
drafting, review, and teaching workflows.

By contrast, generic grammar checkers mainly flag spelling, punctuation, and local grammar. They usually do not evaluate cross-sentence links, section progression, or equation-to-prose
explanation. Hermeneia audits those higher-level signals and reports evidence, confidence, and
rationale for each finding.

### Advantages

- Diagnose clarity issues from sentence wording to document organization.
- Apply profile-specific policies for research, pedagogical, and mathematical writing.
- Attach evidence, confidence, and rationale to each rule outcome so reviewers can audit decisions.
- Order revision steps by structural dependency instead of lexicographic rule order.
- Validate configuration strictly, apply explicit merge semantics, and fail early on unknown fields or rule ids.

---

## Features

Current input support is Markdown (`.md`, `.markdown`).

- [x] Parse Markdown (`.md`, `.markdown`) into block/inline Document IR with stable block ids, sentence ids, and source spans.
- [x] Build and share `DocumentIndexes`, `SourceLine` structural views, and `FeatureStore` across all rule families.
- [x] Classify rules as `SourcePatternRule`, `AnnotatedRule`, or `HeuristicSemanticRule`.
- [x] Cover surface, discourse, paragraph, structure, audience, and math domains with first-party rules.
- [x] Emit text and JSON reports with evidence-bearing diagnostics.
- [x] Compute weighted hierarchical scores and let configuration control score outputs.
- [x] Build revision plans and emit conservative deterministic rewrites when preconditions hold.
- [x] Pin annotation behavior with snapshots and keep warm-run benchmark artifacts under version control.
- [ ] Add first-party language packs beyond English.
- [ ] Support scoring aggregation strategies beyond `hierarchical`.
- [ ] Add reporting adapters, including SARIF and HTML.
- [ ] Integrate with editors and LSP clients for in-editor diagnostics.
- [ ] Parse native LaTeX (`.tex`) sources directly.
- [ ] Compute prose metrics directly during lint runs and expose them in reports.
- [ ] Rewrite source files in place automatically.

---

## Quick Start

Quick Start provides one command-line run and one import check.

### CLI

Run the linter on a Markdown file:

```sh
hermeneia lint notes.md --profile research
```

### Application Programming Interface

Check that the package is importable in the active environment:

```python
import hermeneia

hermeneia.info()
```

---

## Documentation

Recommended reading order:

1. Writing Quality Model
2. Rule Registry
3. Metrics
4. Usage
5. Configuration
6. CLI Reference
7. Prose Audit Protocol

| Guide | Content |
| ----- | ------- |
| [Installation](docs/guide/installation.md) | Prerequisites and source setup |
| [Usage](docs/guide/usage.md) | Common analysis workflows and rule filtering |
| [CLI Reference](docs/guide/cli-reference.md) | Command and option reference |
| [Configuration](docs/guide/configuration.md) | Schema, resolution layers, and merge semantics |
| [Prose Audit Protocol](docs/guide/prose-audit-protocol.md) | Manual audit workflow, severity model, and verdict contract |
| [Writing Quality Model](docs/guide/writing-quality-model.md) | Conceptual quality rationale and readability baseline |
| [Metrics](docs/guide/metrics.md) | Readability metrics, formulas, and interpretation limits |
| [Sources and Further Reading](docs/guide/sources-and-further-reading.md) | External sources and supporting tools |
| [Internals](docs/internals/index.md) | Architecture, pipeline, and extension seams |
| [Architecture Decisions](docs/adr/index.md) | Accepted design decisions and rejected alternatives |

Full API documentation and rendered guides are also available at
[esther-poniatowski.github.io/hermeneia](https://esther-poniatowski.github.io/hermeneia/).

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

---

## Acknowledgments

### Authors

**Author**: @esther-poniatowski

For academic use, the GitHub "Cite this repository" feature generates citations in
various formats. The [citation metadata](CITATION.cff) file is also available.

---

## License

Hermeneia is licensed under the terms of the
[GNU General Public License v3.0](LICENSE).
