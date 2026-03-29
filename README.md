# hermeneia

[![Conda](https://img.shields.io/badge/conda-eresthanaconda--channel-blue)](#installation)
[![Maintenance](https://img.shields.io/maintenance/yes/2026)]()
[![Last Commit](https://img.shields.io/github/last-commit/esther-poniatowski/hermeneia)](https://github.com/esther-poniatowski/hermeneia/commits/main)
[![Python](https://img.shields.io/badge/python-%E2%89%A53.12-blue)](https://www.python.org/)
[![License: GPL](https://img.shields.io/badge/License-GPL--3.0-yellow.svg)](https://opensource.org/licenses/GPL-3.0)

Diagnoses and improves research, pedagogical, and mathematical writing through profile-aware, stratified rule systems.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Documentation](#documentation)
- [Support](#support)
- [Contributing](#contributing)
- [Acknowledgments](#acknowledgments)
- [License](#license)

## Overview

Hermeneia is a writing diagnostics engine for research notes, lecture expositions, and pedagogical explanations. It detects formulations that hinder clarity or flow, proposes concrete revisions, and scores text quality at every level of organization — from individual sentences to the document as a whole.

### Motivation

Research and pedagogical writing must sustain two properties at once: conceptual depth and expositional accessibility. Standard academic prose, shaped by peer-review conventions, favors lexical density and syntactic complexity over the communicative properties that support knowledge transfer. Generalist AI writing assistants do not solve this problem — they systematically regress toward academic conventions, either preserving technical depth at the cost of readability or gaining apparent simplicity by sacrificing precision.

Hermeneia takes a different path. Rather than delegating quality judgment to an unconstrained language model, it encodes writing-quality criteria as explicit, auditable rules grounded in reader-expectation theory, discourse analysis, and plain-language research. Every diagnostic finding is traceable to a declared rule, every threshold is adjustable per context, and the full system behavior is inspectable and reproducible.

### Advantages

- **Profile-aware**: the same rule inventory produces different assessments for a lecture note, a research abstract, and a tutorial, by adapting thresholds and active rules to the declared audience, genre, section, and register.
- **Auditable**: no implicit criteria — every finding names the rule that triggered it, the principle that justifies it, and the text span it applies to.
- **Configurable without code changes**: all rules, severities, thresholds, and suggestion modes are declared in a YAML schema that the writer controls directly.
- **Grounded in research**: rules derive from reader-expectation principles (Gopen), rhetorical move analysis (Swales), cohesion metrics (Coh-Metrix), and plain-language conventions — not ad hoc stylistic preferences.
- **Revision-aware**: suggestions respect a dependency order (reorganize structure, then link sentences, then rewrite locally), so local polishing never masks structural problems.

---

## Features

### Detection

- [ ] **Surface style**: sentence length distribution, passive voice in topic position, nominalization with weak verb support, prepositional chain length, noun cluster density.
- [ ] **Local discourse**: subject–verb distance, subordinate clause load, stress-position placement, pronominal reference coherence, topic continuity between adjacent sentences.
- [ ] **Paragraph rhetoric**: topic sentence presence and placement, mixed-topic detection, rhetorical move identification, sentence-length rhythm.
- [ ] **Document structure**: heading parallelism, orphan sections, abstract-to-body alignment, cross-paragraph semantic redundancy, section weight balance.
- [ ] **Audience fit**: definition-before-use tracking, acronym burden, hedge-word appropriateness, claim-evidence calibration, jargon density relative to audience profile.

### Revision Suggestions

- [ ] **Deterministic rewrites**: nominalization reversal, passive-to-active conversion, sentence splitting, prepositional chain reduction.
- [ ] **Guided suggestions**: rubric-constrained proposals for discourse-level and semantic violations, each citing the specific criterion addressed.

### Scoring and Reporting

- [ ] **Hierarchical scoring**: per-layer quality breakdown (surface, discourse, paragraph, document, audience) instead of a single opaque number.
- [ ] **Diagnostic reports**: ranked violations by severity and layer, with localized span annotations on the input text.
- [ ] **Revision plans**: ordered revision operations that respect the structural dependency between layers.

---

## Installation

### Using pip

Install from the GitHub repository:

```bash
pip install git+https://github.com/esther-poniatowski/hermeneia.git
```

### Using conda

Install from the eresthanaconda channel:

```bash
conda install hermeneia -c eresthanaconda
```

### From source

1. Clone the repository:

      ```bash
      git clone https://github.com/esther-poniatowski/hermeneia.git
      ```

2. Create a dedicated virtual environment and install:

      ```bash
      cd hermeneia
      conda env create -f environment.yml
      conda activate hermeneia
      ```

---

## Quick Start

### CLI

```sh
hermeneia --help
```

### Python

```python
import hermeneia

hermeneia.info()
```

---

## Documentation

- [User Guide](https://esther-poniatowski.github.io/hermeneia/guide/)
- [API Documentation](https://esther-poniatowski.github.io/hermeneia/api/)
- [Project Proposal](docs/proposal.md)

> [!NOTE]
> Documentation can also be browsed locally from the [`docs/`](docs/) directory.

---

## Support

**Issues**: [GitHub Issues](https://github.com/esther-poniatowski/hermeneia/issues)

**Email**: `esther.poniatowski@ens.psl.eu`

---

## Contributing

Please refer to the [contribution guidelines](CONTRIBUTING.md).

---

## Acknowledgments

### Authors & Contributors

**Author**: @esther-poniatowski

**Contact**: `esther.poniatowski@ens.psl.eu`

For academic use, please cite using the GitHub "Cite this repository" feature to
generate a citation in various formats.

Alternatively, refer to the [citation metadata](CITATION.cff).

### Theoretical Foundations

Hermeneia's rule inventory is grounded in the following traditions:

- **Reader-expectation theory** (George Gopen) — information placement and sentence-level fluidity
- **Rhetorical move analysis** (John Swales, Academic Phrasebank) — paragraph and section-level discourse structure
- **Cohesion and discourse metrics** (Coh-Metrix) — referential continuity and connective structure as predictors of comprehension
- **Plain-language conventions** — empirically grounded surface heuristics for general accessibility

---

## License

This project is licensed under the terms of the [GNU General Public License v3.0](LICENSE).
