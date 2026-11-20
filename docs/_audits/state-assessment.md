# Development state of hermeneia

The defects that block further work on hermeneia are stated below, with their evidence and with the decisions taken on 2026-10-23. The actions that remove these defects are tracked in the [open work of hermeneia](../../TODO.md). Two companion reports detail the [conflicts with the oikos style](oikos-style-conflicts.md) and the [boundary with the geonexus checkers](geonexus-boundary.md).

## Baseline

The measurements were taken on 2026-10-23, against the following state:

- hermeneia at commit `d7e525c`, in the conda environment `hermeneia`, with spaCy 3.8.16 and the model `en_core_web_sm` 3.8.0;
- 94 rules, and a test suite of 291 tests, all passing;
- oikos at commit `7c1929a`, and geonexus at commit `b32ed7d5`.

Precision was measured on two corpora:

- **Exemplars.** The target versions of six exemplars of `writing-exemplars`, the calibration examples of the oikos style, totalling 211 words. The six cover the main kinds of text (the expository and motivating paragraphs, the opening sentence, the contrast, the repair and the documentation sentence). Each of their sentences follows the oikos style, so every finding on them is a false positive.
- **geonexus rules.** The notes of `docs/rules/` in geonexus, totalling 35,227 words, linted from the root of the vault with its `.hermeneia.yaml`. These notes were written and audited under the oikos rules.

## Decisions

Three architecture decisions were taken on 2026-10-23:

- the [reference style of hermeneia](../adr/0006-oikos-style-as-reference.md) is the oikos style;
- the [specification of every prose rule](../adr/0007-rule-specifications-in-yaml.md) moves into a YAML file of hermeneia, and the Python code documents only the implementation;
- [sentence-level prose](../adr/0008-geonexus-boundary.md) belongs to hermeneia, and no geonexus checker may carry that concern.

## Findings

### Precision

| Corpus | Words | Findings | Findings per 100 words | Errors |
| --- | --- | --- | --- | --- |
| Exemplars | 211 | 36 | 17.1 | 11 |
| geonexus rules | 35,227 | 3,444 | 9.8 | 752 |

On the exemplars, five rules produce 31 of the 36 findings:

- `vocabulary.nominalization`: 11 errors;
- `linkage.transition_quality`: 8 findings at severity `info`;
- `syntax.passive_voice`: 6 warnings;
- `syntax.embedding_depth`: 4 warnings;
- `linkage.indefinite_opening`: 2 findings at severity `info`.

On the geonexus rules, `vocabulary.nominalization` alone produces 627 of the 752 errors, despite the 26 nouns declared as project terms by the configuration of the vault. After that rule come `linkage.transition_quality` (315 findings) and `syntax.passive_voice` (276, lowered to `info` by the vault).

The oikos rule `discharge-each-finding` requires each finding to be quoted, with a justified disposition. At almost ten findings per 100 words, that requirement cannot be met by an agent or a person on a text of a few pages. Consequently, the projects running hermeneia, geonexus among them, silence its findings in their configuration instead of fixing their prose.

Four causes produce the noise:

- **Lexical matching.** `vocabulary.nominalization` flags a noun by its suffix, so it reports nouns denoting entities, such as `action` and `section`.
- **Overlap heuristics.** `linkage.transition_quality`, `paragraph.topic_sentence` and `structure.opening_message_focus` decide from the share of words common to two sentences, and fire on paragraphs that carry their topic through the subject slot.
- **Conflicts with the oikos style.** Several rules ban constructions prescribed by oikos, such as a fronted sentence adverbial or a passive keeping the topic as subject.
- **Severity.** Several heuristic rules report at severity `error` (among them `vocabulary.nominalization`, `vocabulary.abstract_compound_modifier`, `linkage.banned_transition` and `reference.structural_metalanguage`).

### Natural-language processing

The parser is active. Each run loads spaCy with `en_core_web_sm` and emits no diagnostic of fallback. Moreover, the findings of `syntax.passive_voice` cite a dependency signal as evidence. Therefore, the noise originates in the rules that read the parse, not in a missing component.

The annotator leaves part of the parse unused:

- four attributes of each token are kept (the lemma, the coarse part of speech, the dependency label and the head);
- four other annotations are dropped (the fine tag such as `VBN`, the morphology, the noun chunks and the entities).

Moreover, the annotator parses each sentence by a separate call to spaCy instead of a batch through `nlp.pipe`, and a run on the geonexus corpus takes 16 seconds.

Eighteen rule modules read the attributes of the parse directly. The other rules match patterns and lexicons on the text, some of them through the lemma-aware helpers of `rules/common.py`.

The optional embeddings backend is inactive. The configuration defaults to `backend: none`, and the package `sentence-transformers` is not installed. Only `paragraph.paragraph_redundancy` would consume the backend.

### Work tracking

The file `TODO` holds a note on a wrapper for `mypy`, and that note concerns no work on hermeneia. The open work is spread over the unchecked items of the former alignment report and the unchecked features of the README, with no checklist that orders it.

### Rule specifications

Four defects concern how rules are declared and documented:

- The metadata of a rule lives only in code, in `RuleMetadata`. That class lacks every documentary field, such as the rationale, the examples and the oikos counterpart. The [rule registry](../guide/rule-registry.md) documents these fields by hand, and it disagrees with the code: it calls `syntax.passive_voice` "Active opening preference", whereas the rule flags every passive.
- Planted cases that must fire or must pass exist for 13 of the 94 rules, in `tests/fixtures/rule_cases.yaml`.
- Rules are declared in two ways: 11 rules through the helper `clause_metadata`, and 83 through a direct call to `RuleMetadata`.
- Configuration is declared in several places. The membership of a rule in a profile is stated both in the `active_rules` of four presets and in `RuleMetadata.profiles_active`. The threshold of `syntax.sentence_length` is set in the rule, in the language pack and in each profile.

### Correspondence with oikos

The alignment report was filed among the architecture notes in `docs/internals/`, although it records open work rather than architecture. The report now sits in this folder, split in two: the [coverage inventory](oikos-rule-alignment.md) and the [conflict report](oikos-style-conflicts.md). The conflict report records three results new to this audit:

- the conflicts recorded on 2026-09-26 all remain open;
- four new conflicts appear on the exemplars;
- three model sentences of oikos break another oikos rule.

The correspondence also exists in a second copy: the table of linter rules in the oikos `audit-protocol`, maintained by hand. Moreover, that protocol lets the linter read "the `.hermeneia.yaml` nearest to the target". However, oikos holds no such file, so its instruction files are linted with the default profile.

### Overlap with geonexus

Six kinds of finding of the geonexus checkers test the form of prose strings. hermeneia already tests that form through `structure.field_form`. Three further groups of kinds read words or link fragments, and their owner is undecided. The [changes needed in hermeneia](geonexus-boundary.md) are listed beside each kind.

### Documentation and repository

Six smaller defects remain:

- The help of `--format` lists `text` and `json`, whereas the CLI also implements `compact`, the format used by the oikos protocol.
- `hermeneia --help` prints the numpydoc sections of the docstrings, such as "Input value for ``version``". Moreover, several docstrings are placeholders, such as "Passivevoicerule.".
- The README names the Rule Registry in its reading order, but its table of guides omits it. The README also misspells "lose" as "loose".
- `pyproject.toml` opens on the template header, with its placeholders.
- The [metrics guide](../guide/metrics.md) documents readability metrics that no code computes.
- `coverage.xml` lies untracked at the root of the repository and is absent from `.gitignore`.

## Proposed solutions

### Calibration corpus

Over-firing must become a measured quantity before any rule is refined. A calibration corpus in `tests/fixtures/calibration/` holds two parts:

- conforming prose, gathered from the exemplars of oikos and from a frozen copy of audited geonexus notes;
- planted violations, gathered from the ✗ versions of the exemplars and from the probes of the conflict report.

A test reports the false positives of each rule per 1,000 words of conforming prose. Its counts are frozen as a baseline that may only shrink, and the CI fails on any count above it. Each of the 94 rules receives planted sentences, some that must fire and some that must pass.

### Severity policy

Each severity is reserved for one class of rule:

- `error` for a rule whose matches are certain, such as a contraction, a raw anchor or a link to a heading slug;
- `warning` at most, for a heuristic built on the parse;
- `info`, or the experimental tier disabled by default, for a heuristic built on word overlap, until the calibration corpus fixes its thresholds.

### Refinements built on the parse

Each noisy rule receives a [proposed resolution](oikos-style-conflicts.md) in the conflict report. Most resolutions rely on the parse, as the event reading of a nominalization and the conjuncts of an enumeration show. Consequently, the annotator must keep the fine tag, the morphology and the noun chunks. The annotator must also parse in batches.

### Rule specification schema

Each prose rule receives one YAML file, validated by a JSON Schema in `schemas/rule-spec.schema.json`. The file holds the norm of the rule and its detection, as the [decision on rule specifications](../adr/0007-rule-specifications-in-yaml.md) requires. The code loads the metadata of each hermeneia rule from these files, and the oikos prose modules and the rule registry are generated from them. The fields take their names from the vocabulary drafted by Eutaxis for rule templates (for instance `prescription`, `prohibition` and `rationale`).

```yaml
id: verb-over-process-noun
name: verb over process noun
description: replaces a process noun in subject or object position by its verb
norm:
  prescription: >-
    Use the verb from which a process noun derives, when the verb form is shorter or more direct.
  prohibition: >-
    Do not use a process nominalization in subject or object position.
  exceptions:                 # closed list; a construction outside it is a violation
    - construction: a conventional term naming the property of interest
      example: "proves existence of a solution"
    - construction: a named technical quantity used in distinct sentences of one document
      example: "amplification selectivity"
  examples:
    valid:
      - "Regularization reduces overfitting."
      - "The section states the bound."
    invalid:
      - "The application of regularization results in a reduction of overfitting."
  operational_check: >-
    For each noun in subject or object position, find the verb from which it derives. When that verb exists, the verb replaces the noun.
  rationale: >-
    A process noun states the action of a clause as a noun and leaves its actor unnamed.
detection:
  repair: use the verb, unless the noun is a named technical quantity
  rules:
    - id: vocabulary.nominalization
      coverage: partial       # full | partial
      gaps: [named quantity recurring across sentences]
      method: parse           # lexical | pattern | parse | discourse | semantic
      maturity: experimental  # stable | experimental | retired
      severity: warning
      profiles: [research, strict, mathematical]
      options: {}
```

One schema removes five duplicates at once:

- the norm, stated in oikos and restated in the hermeneia metadata;
- the two ways of declaring a rule;
- the membership in profiles, stated twice;
- the registry, written by hand;
- the separate file of planted cases.

## Reproduction

The measurements can be repeated with the commands below, run in the environment `hermeneia`:

- for the exemplars, write each target version named in the baseline as one paragraph of a single Markdown file, then run `hermeneia lint <file> --profile research --format json`;
- for the geonexus rules, run `hermeneia lint docs/rules --format json` from the root of the vault;
- for the probes, write each probe of the conflict report under an H1 heading in a file of its own, then run `hermeneia lint <file> --format compact`.
