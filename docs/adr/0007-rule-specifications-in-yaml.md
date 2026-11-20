# ADR 0007: Rule specifications in YAML, held by hermeneia

- Status: Accepted
- Date: 2026-10-23
- Amended: 2026-11-02 by the decision of `geonexus` on [designation and typography](https://github.com/esther-poniatowski/geonexus/blob/584a14f134e7b6231eeae31518622439acf10d00/docs/_decisions/designation-and-typography.md): hermeneia publishes its rule specifications, and the compiler of the instruction modules renders them, so no generator of a consumer format stays in hermeneia.

## Context

A prose rule is stated in up to three places:

- the Markdown text of an oikos module, stating the norm;
- the Python metadata of a hermeneia rule, restating parts of the norm (the label, the default options, the messages and the rationale strings);
- the [rule registry](../guide/rule-registry.md), written by hand.

The copies disagree. For instance, oikos splits a sentence above 30 words, whereas hermeneia applies 22, 28, 30 or 34 words depending on the profile and the layer read. Similarly, the registry names `syntax.passive_voice` after a behavior absent from the code. Moreover, no schema validates the Markdown text, so no tool checks the examples of a rule against its detector.

## Decision

A rule is held by the tool that implements it. Therefore, each prose rule has one specification: a YAML file in hermeneia, validated by a JSON Schema. The specification holds two parts:

- the **norm**, stating what the rule prescribes, prohibits and exempts, with its examples, its rationale and its test;
- the **detection**, stating which hermeneia rules detect the norm and with which settings, such as the severity and the thresholds. A norm enforced by reading alone declares no detector.

All other statements of a rule are generated from its specification:

- the oikos modules within the scope of the decision;
- the table of linter rules in the oikos audit protocol;
- the rule registry of hermeneia.

The Python code documents only the implementation and the aspects relevant to a programmer (its parameters, data flow, architecture, regular expressions and tools). The code reads the name, the severity, the thresholds and the repair of a rule from the specification. No part of the specification is restated in metadata, docstrings or strings.

The decision covers two groups of rules:

- the rules of six oikos modules: the five prose modules (`prose-writing-style`, `sentence-construction`, `prose-structures`, `reasoning-and-exposition`, `referencing-and-citations`) and `mathematical-exposition`, whose norms are detected by the `math.*` rules of hermeneia;
- the rule sets that hermeneia receives in prose from other projects, held in the [rule sources](../rule-sources/index.md) until they migrate, such as the decision rules of research notes received from gnomon.

The names of the fields follow the field vocabulary drafted by Eutaxis for rule templates.

## Alternatives considered

1. **Norm in oikos, detection in hermeneia.** oikos keeps the text of each rule, and each hermeneia specification points to that text. Rejected: one rule keeps two sources that drift apart, and the norm stays outside validation.
2. **Specifications in the Eutaxis template format, held by oikos.** Rejected: hermeneia tests the examples and the thresholds of a rule, so another holder separates a rule from its tests. Moreover, the Eutaxis template format is still undecided.
3. **Specifications in Python metadata.** Rejected: this option mixes the norm with the implementation.

## Consequences

- The oikos modules within the scope become generated files, and hand edits to them stop once generation runs. Therefore, the oikos compiler must read sources from the hermeneia repository, a case raised by the Eutaxis open question on cross-repository sources.
- For the prose rules, the oikos plan to migrate rules to structured templates reduces to generating the prose modules from hermeneia.
- `RuleMetadata` keeps only the binding between a rule identifier and its implementation, together with the data used by the implementation alone (the abstention flags and the evidence fields). The helper `clause_metadata`, the lists `active_rules` of the profiles and the threshold overrides disappear.
- The planted cases of `tests/fixtures/rule_cases.yaml` become the examples of the specifications, and a test runs every example against the detector of its rule.
- The [registration protocol of the rules](0004-unified-rule-registration.md) is unchanged: only the source of the metadata moves.
- One norm can be detected by several hermeneia rules, and one hermeneia rule can detect several norms. Consequently, the unit of a specification is still undecided: one specification per norm, or one per detector.
- A received rule set migrates rule by rule. A received rule that restates the norm of an oikos rule merges into the specification of that norm, so that no norm has two specifications. A received rule without a counterpart receives its own specification.
- Once its rules have migrated, a received rule set is deleted. Every link to it from another project is then repointed to the specifications that replace it.
