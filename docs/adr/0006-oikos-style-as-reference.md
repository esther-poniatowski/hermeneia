# ADR 0006: Oikos style as the reference style

- Status: Accepted
- Date: 2026-10-23

## Context

oikos runs hermeneia as the linter of its prose style, yet the two rule sets disagree on 18 points, recorded as [conflicts with the oikos style](../_audits/oikos-style-conflicts.md). On the worked exemplars of the oikos style, hermeneia reports 17 findings per 100 words, all of them false positives. Consequently, the projects running hermeneia silence its findings in their configuration instead of repairing their prose.

## Decision

The oikos prose style is the reference style of hermeneia. When a hermeneia rule and a rule of that style disagree, the hermeneia rule changes. When two rules of the style contradict each other, the style itself is corrected.

The [specification of the style](0007-rule-specifications-in-yaml.md) moves into hermeneia. Therefore, "oikos style" names a style, not the repository that holds its specification.

## Alternatives considered

1. **Style-neutral hermeneia, with an oikos style pack.** hermeneia would keep its own defaults and load the oikos style as one configuration among others. Rejected: under this option, each conflict requires two behaviors in the code, although the only consumer of hermeneia applies one style.
2. **hermeneia rules as the reference.** oikos would adapt its rules to hermeneia. Rejected: the oikos rules are calibrated on worked exemplars, whereas the hermeneia rules report findings on every exemplar of that style.

## Consequences

- Each conflict receives a verdict, and by default the hermeneia rule changes.
- Three model sentences of the style break another rule of the style, so each must be rewritten.
- A hermeneia rule with no counterpart in the style needs a status (an extension, a proposal to the style, or a retirement). The status of each such rule is still undecided.
