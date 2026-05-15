# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added

- New reference rules:
  - `reference.citation_as_agent`
  - `reference.citation_tail_parenthetical`
  - `reference.structural_metalanguage`
- New vocabulary rules:
  - `vocabulary.cardinality_framing`
  - `vocabulary.filler_noun_scaffolding`
- New syntax rule:
  - `syntax.multi_action_sentence`
- New structure rule:
  - `structure.declarative_heading`
- Shared citation-style resolver used by reference citation rules, with built-in styles:
  - `key_year_bracket`
  - `key_bracket`
  - `numeric_bracket`
  - `author_year_parenthetical`
  - `pandoc_citekey`

### Changed

- Citation-related rule options now support style-based and multi-pattern matching:
  - `citation_styles`
  - `citation_tag_pattern`
  - `citation_tag_patterns`
- `reference.citation_as_agent` now validates and resolves citation detection from both selected
  built-in citation styles and custom regex patterns.
- `reference.citation_tail_parenthetical` now validates and resolves citation detection from both
  selected built-in citation styles and custom regex patterns.
- Configuration resolution now fails early for unknown `citation_styles` values in citation rule
  overrides.
- Profile catalog includes an explicit `strict` profile variant for tighter prose constraints.

### Documentation

- Configuration guide now documents rule options for:
  - citation rules
  - structural metalanguage
  - multi-action sentences
  - cardinality framing
  - filler noun scaffolding
  - declarative headings
