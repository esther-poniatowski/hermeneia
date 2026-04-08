# Architecture

Hermeneia follows a layered architecture aligned with Domain, Application, Infrastructure, and Adapters.

## Layer Mapping

| Layer | Primary Modules | Responsibility |
| --- | --- | --- |
| Domain | `document/model.py`, `rules/base.py`, rule modules, scoring/revision/report DTOs | Pure analysis concepts: spans, blocks, sentences, violations, rule metadata/contracts |
| Application | `engine/runner.py`, `engine/detector.py`, `config/profile.py` | Orchestration, sequencing, profile resolution, rule dispatch, failure boundaries |
| Infrastructure | `document/markdown.py`, `document/annotator.py`, `infrastructure/embeddings.py`, `config/loader.py` | External effects and integrations (parser, spaCy, embedding backend, YAML I/O) |
| Adapters | `cli.py` | CLI parsing, composition root wiring, text/json rendering |

## Dependency Direction

- Adapters depend on Application + Infrastructure wiring.
- Application depends on Domain contracts and infrastructure protocols.
- Domain stays reusable and side-effect-free.

## Core Runtime Object Graph

`cli.py` composes:

- `RuleRegistry` + built-in/external rule loading
- `LanguagePack` from registry
- `ResolvedProfile` from `ProfileResolver`
- `AnalysisRunner` with:
  - `MarkdownDocumentParser`
  - `SpaCyDocumentAnnotator`
  - optional embedding backend
  - runtime policy (scoring/suggestions/debug)

## Stability Contracts

- Rule ids are stable dotted identifiers.
- Rule metadata is the canonical declaration for severity, layer, tractability, language support, and evidence contract.
- `Document` + `DocumentIndexes` + `FeatureStore` form the shared source of truth for downstream rule logic.
