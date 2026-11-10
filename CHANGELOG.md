# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Changed (command line)

The command line follows the command-line conventions of the workspace. The former names are retired without an alias.

- The settings file `.hermeneia.yaml` or `.hermeneia.yml` is renamed `hermeneia.yml`, and is read from `config/tools/hermeneia.yml` or `hermeneia.yml` below the root of the run. Both files existing is an error naming both.
- The settings file is no longer searched upwards from the first target. The root of the run is resolved from `--root`, then the environment variable `HERMENEIA_ROOT`, then the nearest ancestor of the current folder holding the settings file, then the current folder.
- The `path` globs of `terminology.files` resolve against the root of the run, no longer against the folder of the settings file.
- `--root` names the root of the run in every format; it no longer requires `--format sarif`, and takes the short form `-r`.
- `--output` writes the report of every format, and takes the short form `-o`; `--config` takes the short form `-c`.
- `--version` and `-v` print the version; they formerly stopped on a missing command.

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
