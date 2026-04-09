# hermeneia

[![Conda](https://img.shields.io/badge/conda-eresthanaconda--channel-blue)](docs/guide/installation.md)
[![Maintenance](https://img.shields.io/maintenance/yes/2026)]()
[![Last Commit](https://img.shields.io/github/last-commit/esther-poniatowski/hermeneia)](https://github.com/esther-poniatowski/hermeneia/commits/main)
[![Python](https://img.shields.io/badge/python-%E2%89%A53.12-blue)](https://www.python.org/)
[![License: GPL](https://img.shields.io/badge/License-GPL--3.0-yellow.svg)](https://opensource.org/licenses/GPL-3.0)

Checks and improves research, pedagogical, and mathematical writing with profile-aware, stratified rules.

---

## Table of Contents

- [hermeneia](#hermeneia)
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

Technical and mathematical writing often obscures the intended claim and line of reasoning. This
problem appears when prose turns actions into nouns, weakens links between ideas, or targets the
wrong audience. Generic grammar checkers usually flag local form issues, such as spelling,
punctuation, and sentence-level grammar, but they do not assess higher-level properties of the
exposition, such as fluidity, clarity, accessibility, and explicitness.

Hermeneia addresses this gap with a layered quality model: surface directness, discourse linkage,
paragraph progression, document structure, audience calibration, and math exposition discipline.
It combines rule-based diagnostics with supporting signals (for example, sentence length, passive
rate, and readability indices) so users can prioritize edits by reader impact instead of by
cosmetic style preferences.

### Advantages

- Diagnose writing across surface style, local discourse, paragraph rhetoric, document structure, audience fit, and mathematical conventions.
- Activate profile-aware rule sets and severities for research, pedagogical, and math workflows.
- Attach evidence, confidence, and rationale to each rule outcome so reviewers can audit decisions.
- Order revision steps by structural dependency instead of lexicographic rule order.
- Validate configuration strictly, apply explicit merge semantics, and fail early on unknown fields or rule ids.

---

## Features

- [x] Parse Markdown into block/inline Document IR with stable block ids, sentence ids, and source spans.
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
- [ ] Rewrite source files in place automatically.

---

## Quick Start

### CLI

```sh
hermeneia lint notes.md --profile research
```

### Application Programming Interface

```python
import hermeneia

hermeneia.info()
```

---

## Documentation

Read the documentation in this order when onboarding a project:
quality model -> rule inventory -> usage workflow -> configuration controls -> CLI details -> audit protocol.

| Guide | Content |
| ----- | ------- |
| [Installation](docs/guide/installation.md) | Prerequisites and source setup |
| [Usage](docs/guide/usage.md) | Common analysis workflows and rule filtering |
| [CLI Reference](docs/guide/cli-reference.md) | Command and option reference |
| [Configuration](docs/guide/configuration.md) | Schema, resolution layers, and merge semantics |
| [Prose Audit Protocol](docs/guide/prose-audit-protocol.md) | Manual audit workflow, severity model, and verdict contract |
| [Writing Quality Model](docs/guide/writing-quality-model.md) | Conceptual quality rationale and readability baseline |
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
