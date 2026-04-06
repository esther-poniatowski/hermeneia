# hermeneia

[![Conda](https://img.shields.io/badge/conda-eresthanaconda--channel-blue)](docs/guide/installation.md)
[![Maintenance](https://img.shields.io/maintenance/yes/2026)]()
[![Last Commit](https://img.shields.io/github/last-commit/esther-poniatowski/hermeneia)](https://github.com/esther-poniatowski/hermeneia/commits/main)
[![Python](https://img.shields.io/badge/python-%E2%89%A53.12-blue)](https://www.python.org/)
[![License: GPL](https://img.shields.io/badge/License-GPL--3.0-yellow.svg)](https://opensource.org/licenses/GPL-3.0)

Diagnoses and improves research, pedagogical, and mathematical writing through
profile-aware, stratified rule systems.

---

## Table of Contents

- [hermeneia](#hermeneia)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
    - [Motivation](#motivation)
    - [Advantages](#advantages)
    - [Theoretical Foundations](#theoretical-foundations)
  - [Features](#features)
    - [Detection](#detection)
    - [Revision Suggestions](#revision-suggestions)
    - [Scoring and Reporting](#scoring-and-reporting)
  - [Quick Start](#quick-start)
  - [Documentation](#documentation)
  - [Contributing](#contributing)
  - [Acknowledgments](#acknowledgments)
    - [Authors](#authors)
  - [License](#license)

## Overview

### Motivation

Technical and mathematical writing requires precise control over sentence structure,
terminology, and logical flow. Surface-level style checkers flag grammar issues but miss
deeper structure and formulation issues that degrade readability, comprehension and engagement.
Typical examples that pervade technical writing include nominalizations that obscure agency,
abstract framing that buries results, and compound modifiers that compress relationships.

### Advantages

- **Stratified rule system** — rules are organized into five layers (surface style,
  local discourse, paragraph rhetoric, document structure, audience fit), each targeting
  a distinct level of textual organization.
- **Profile-aware analysis** — writing profiles (research, pedagogical, mathematical)
  activate the rule subsets and severity levels appropriate to the genre.
- **Hard blockers** — critical rules (nominalization, abstract framing, bare pronouns,
  bare symbols) function as hard blockers that gate output.
- **Auditable diagnostics** — each finding names the triggering rule, the justifying
  principle, and the text span it applies to.
- **Declarative configuration** — all rules, severities, thresholds, and suggestion
  modes are declared in a YAML schema, adjustable without code changes.
- **Layered revision order** — suggestions follow a dependency order (restructure, then
  link sentences, then rewrite locally), so local polishing never masks structural
  problems.

### Theoretical Foundations

The rule system draws on reader-expectation theory (Gopen & Swan), plain-language
research (Cutts, Garner), and mathematical writing practice (Halmos, Knuth).

---

## Features

### Detection

- [ ] **Surface style**: Detect sentence-length anomalies, passive voice in topic
  position, nominalizations with weak verb support, long prepositional chains, and
  dense noun clusters.
- [ ] **Local discourse**: Check subject–verb distance, subordinate clause load,
  stress-position placement, pronominal reference coherence, and topic continuity
  between adjacent sentences.
- [ ] **Paragraph rhetoric**: Verify topic-sentence presence and placement, mixed-topic
  paragraphs, rhetorical move sequences, and sentence-length rhythm.
- [ ] **Document structure**: Validate heading parallelism, orphan sections,
  abstract-to-body alignment, cross-paragraph semantic redundancy, and section weight
  balance.
- [ ] **Audience fit**: Evaluate definition-before-use ordering, acronym burden,
  hedge-word appropriateness, claim-evidence calibration, and jargon density relative
  to the audience profile.

### Revision Suggestions

- [ ] **Deterministic rewrites**: Reverse nominalizations, convert passive to active
  voice, split overloaded sentences, and reduce prepositional chains.
- [ ] **Guided suggestions**: Propose rubric-constrained revisions for discourse-level
  and semantic violations, each citing the specific criterion addressed.

### Scoring and Reporting

- [ ] **Hierarchical scoring**: Break down quality per layer (surface, discourse,
  paragraph, document, audience) instead of a single opaque score.
- [ ] **Diagnostic reports**: Rank violations by severity and layer with localized span
  annotations on the input text.
- [ ] **Revision plans**: Order revision operations to respect the structural dependency
  between layers.

---

## Quick Start

Analyze a document:

```sh
hermeneia lint document.md --profile research
```

Apply the mathematical writing profile:

```sh
hermeneia lint notes/ --profile math
```

---

## Documentation

| Guide | Content |
| ----- | ------- |
| [Installation](docs/guide/installation.md) | Prerequisites, pip/conda/source setup |
| [Usage](docs/guide/usage.md) | Workflows and detailed examples |
| [CLI Reference](docs/guide/cli-reference.md) | Full command registry and options |
| [Configuration](docs/guide/configuration.md) | Profiles, rule selection, severity |
| [Writing Standards](docs/standards/writing-standards.md) | The style rules enforced by hermeneia |
| [Math Style Rules](docs/rules/math-style-hard-rules.md) | Hard blockers for mathematical writing |

Full API documentation and rendered guides are also available at
[esther-poniatowski.github.io/hermeneia](https://esther-poniatowski.github.io/hermeneia/).

---

## Contributing

Contribution guidelines are described in [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Acknowledgments

### Authors

**Author**: @esther-poniatowski

For academic use, the GitHub "Cite this repository" feature generates citations in
various formats. The [citation metadata](CITATION.cff) file is also available.

---

## License

This project is licensed under the terms of the
[GNU General Public License v3.0](LICENSE).
