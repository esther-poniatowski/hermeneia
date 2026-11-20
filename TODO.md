# TODO

The open work on hermeneia is ordered by dependency. The evidence behind each action is recorded in the [development state of hermeneia](docs/_audits/state-assessment.md). A step may be taken before its phase when it does not depend on the output of an earlier phase.

## Constraints

- The [reference style](docs/adr/0006-oikos-style-as-reference.md) is the oikos prose style.
- The [specification of each prose rule](docs/adr/0007-rule-specifications-in-yaml.md) is one YAML file in hermeneia, and the Python code documents only the implementation.
- [Sentence-level prose](docs/adr/0008-geonexus-boundary.md) belongs to hermeneia, and no geonexus checker carries that concern.

## Open questions

- **Scope of the migration.** The decision on specifications covers the five prose modules of oikos, `mathematical-exposition` and the rule sets received in prose. Two other rule sets await a decision on whether they migrate too (`markdown-syntax` and the linter rules of `audit-protocol`).
- **Unit of a specification.** A specification may be keyed by norm or by detector, since one norm can be detected by several hermeneia rules and one hermeneia rule can detect several norms.
- **Verdicts on the conflicts.** Each [conflict with the oikos style](docs/_audits/oikos-style-conflicts.md) awaits a verdict, and so do the two decisions required at the end of the conflict report.
- **Owners at the geonexus boundary.** Three groups of kinds of finding have no owner yet (the terms bound by a glossary, the symbols bound by a notation file and the fragments of a link).

## Hygiene

- [ ] List `compact` in the help of `--format`, and keep the numpydoc sections out of the help of the CLI.
- [ ] Replace the placeholder docstrings of the rule modules with docstrings that document the implementation.
- [ ] Add the Rule Registry to the table of guides of the README, and correct "loose" into "lose".
- [ ] Fill or delete the template header of `pyproject.toml`.
- [ ] Decide whether the readability metrics of the [metrics guide](docs/guide/metrics.md) must be computed by the code, or marked as not implemented.

## Measurement

- [ ] Build the calibration corpus in `tests/fixtures/calibration/`, with conforming prose and planted violations.
- [ ] Report the false positives of each rule per 1,000 words of conforming prose, and freeze the counts as a baseline.
- [ ] Make the CI fail on any count above the baseline.

## Rule specifications

- [ ] Settle the scope of the migration and the unit of a specification.
- [ ] Write the JSON Schema of the specifications, with a norm part and a detection part, and with field names aligned with the Eutaxis vocabulary.
- [ ] Migrate each oikos prose rule into a specification, starting with the rules detected by hermeneia.
- [ ] Migrate the [decision rules](docs/rule-sources/decision-rules.md) rule by rule. Compare the full text of each rule with the oikos rules, merge each rule that restates an oikos norm into the specification of that norm, and write a specification for each rule without a counterpart. A comparison of labels suggests counterparts in `reasoning-and-exposition` and `mathematical-exposition` for non-redundancy, functional motivation, deductive continuity, proof strategies, premise legitimacy, intra-unit ordering, mathematical exposition and display, objective unity and local necessity. The same comparison finds no counterpart for scope admissibility.
- [ ] Delete the decision rules once migrated, and repoint the link of the [gnomon note on reasoning and argumentation principles](https://github.com/esther-poniatowski/gnomon/blob/main/docs/references/reasoning-argumentation-principles-cross-field.md) to the specifications that replace them. The link targets `docs/rule-sources/decision-rules.md`.
- [ ] Load the metadata of each hermeneia rule from the specifications, and remove the duplicate declarations (`clause_metadata`, the lists `active_rules` and the threshold overrides of the profiles).
- [ ] Remove from the Python code every restatement of a rule (labels, rationale strings, descriptions of the norm in docstrings), and keep the documentation of the implementation.
- [ ] Turn `tests/fixtures/rule_cases.yaml` into examples of the specifications, and write examples for the 81 rules without planted cases.
- [ ] Test every example against the detector of its rule.
- [ ] Generate the rule registry from the specifications, and test that the identifiers of the code and of the specifications coincide.

## Precision

These actions depend on the measurement phase.

- [ ] Apply the severity policy of the assessment.
- [ ] Extend the annotator to the four annotations dropped today (the fine tag, the morphology, the noun chunks and the entities), and parse in batches.
- [ ] Apply the verdicts on the noisy rules, starting with `vocabulary.nominalization` and `syntax.passive_voice`.
- [ ] Move `linkage.transition_quality`, `paragraph.topic_sentence` and `structure.opening_message_focus` to the experimental tier until the calibration corpus fixes their thresholds.

## Alignment with oikos

These actions depend on the specification phase. The actions owned by oikos are listed in its own task list.

- [ ] Record a verdict on each conflict, and carry each settled conflict into its specification.
- [ ] Provide the export from which oikos generates its prose modules and the table of linter rules of its audit protocol.

## Boundary with geonexus

The actions owned by geonexus are listed in its own task list.

- [ ] Add the [tests missing from `structure.field_form`](docs/_audits/geonexus-boundary.md), so that geonexus can retire its checks of the form of prose strings.
- [ ] Decide with geonexus the owner of each of the three groups of kinds left without one.
