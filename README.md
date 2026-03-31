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

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [Acknowledgments](#acknowledgments)
- [License](#license)

## Overview

### Motivation

Technical and mathematical writing requires precise control over sentence structure,
terminology, and logical flow. Surface-level style checkers flag grammar issues but miss
deeper problems: nominalizations that obscure agency, bare pronouns after display
equations, abstract framing that buries results, and compound modifiers that compress
relationships beyond readability.

### Advantages

- **Stratified rule system** — rules are organized into five layers (surface style,
  local discourse, paragraph rhetoric, document structure, audience fit), each targeting
  a distinct level of textual organization.
- **Profile-aware analysis** — writing profiles (research, pedagogical, mathematical)
  activate the rule subsets and severity levels appropriate to the genre.
- **Hard blockers** — critical rules (nominalization, abstract framing, bare pronouns,
  bare symbols) function as hard blockers that gate output.
- **Mechanical enforcement** — forbidden-string searches and rewrite operators apply
  deterministically, not as advisory suggestions.

### Theoretical Foundations

The rule system draws on reader-expectation theory (Gopen & Swan), plain-language
research (Cutts, Garner), and mathematical writing practice (Halmos, Knuth).

---

## Features

- [ ] **Surface style analysis**: Detect nominalizations, verbose preambles, redundant
  lead-ins, and stacked abstract nouns.
- [ ] **Local discourse evaluation**: Check pronoun discipline, modifier discipline,
  and sentence economy.
- [ ] **Paragraph rhetoric analysis**: Verify topic-sentence coverage, logical
  connectors, and information ordering.
- [ ] **Document structure checking**: Validate heading hierarchy, section dependencies,
  and first-sentence quality.
- [ ] **Audience fit assessment**: Evaluate register consistency, jargon density, and
  assumed-knowledge calibration.

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
