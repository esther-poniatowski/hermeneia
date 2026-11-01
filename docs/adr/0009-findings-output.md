# ADR 0009: Findings output for the gate Elenchos

- Status: Accepted. The decision implements the Hermeneia row of the [producer migration](https://github.com/esther-poniatowski/elenchos/blob/main/docs/producer-migration.md) of Elenchos, under its [findings profile](https://github.com/esther-poniatowski/elenchos/blob/main/docs/profile.md).
- Date: 2026-11-01

## Context

The gate Elenchos reads the findings of each domain tool as a log of the Static Analysis Results Interchange Format (SARIF) 2.1.0, written in the findings profile of the gate. The gate builds the identity of each finding from the tool, the rule, the resource, the locus and a discriminator, and a consumer tolerates a finding by listing its identity in a suppressions file. Therefore, the identity of a finding must stay the same when the file changes elsewhere, and must change when the judged text changes.

A violation of hermeneia carries offsets and lines only. Its sentence and block identifiers are counters, so inserting a paragraph shifts them. Therefore, the identity must rest on the judged text instead.

## Decision

The command `lint` accepts `--format sarif`. The log goes to standard output. The option `--output PATH` writes it to a file instead, and creates the missing folders. The option `--root PATH` names the root of the consumer repository, against which the log states every path. The root defaults to the current folder, since Elenchos runs each check from the root of the consumer. The format refuses `--changed`: a run restricted to changed lines would leave the suppressions of every unchanged finding unmatched, and the gate would report them as stale.

Each result holds the identifier of its rule, its level, its message and one location. The level of `info` becomes `note`, since SARIF has no level `info`. The location names the file as `path:<path>` with an empty locus, and its physical location carries the region of the violation. Columns count code points from 1, as SARIF expects under `columnKind: unicodeCodePoints`. Hermeneia analyses a YAML, Python or commit source through its projection to Markdown. The columns of such a source designate positions in the projection, not in the file, so its region holds lines only. The fields `layer`, `confidence`, `rationale`, `rewrite_tactics` and `evidence` go to `properties`, under the prefix `hermeneia/`.

The discriminator holds the text judged by the rule, normalized to NFC with each run of whitespace collapsed to one space. Its form depends on the sentence that holds the span:

- a span equal to a sentence yields that sentence;
- a span within a sentence yields the matched words in brackets, then the sentence: `[It's] It's obvious that the result holds.`;
- a span on the second sentence of a pair, named by the evidence feature `previous_sentence_id`, yields a digest of both sentences;
- a span that no sentence holds, such as a block, a section or a line of code, yields a digest of its text;
- an empty span yields no discriminator, and the gate numbers identical occurrences.

A digest is `sha256:` followed by the first sixteen hexadecimal digits of the SHA-256 of the normalized text. Readable text up to the sentence lets a reader trace a stale suppression to its sentence. A digest above the sentence keeps the identity of a paragraph short.

Every operational diagnostic of the batch states that some rule was not evaluated on some file: a parse failure, an annotation failure, a fallback of the annotation backend, or a rule that failed. In that case, the run declares a failed invocation, with one notification of level `error` per diagnostic, and keeps every result detected. The gate reads such a run as incomplete. The driver lists every registered rule, whether or not the profile activates it.

## Alternatives considered

The criteria are the stability of an identity under edits elsewhere, its change under an edit of the judged text, the readability of a suppression, and the cost to the profile.

| Option | Benefit | Limitation | Verdict |
| --- | --- | --- | --- |
| empty locus, judged text as discriminator | stable under any edit outside the judged text; needs no change to the profile | a sentence repeated in one file shares its identity, and the gate numbers the occurrences | selected |
| heading path as a new locus type `section:`, with the sentence as discriminator | separates a sentence repeated in two sections | takes a new version of the profile; renaming a heading changes the identity of every finding of its section, although no rule judged the heading | rejected |
| sentence identifier or offset as locus | already computed | shifts whenever text is inserted earlier | rejected |
| readable text at every granularity | every suppression names its text | a paragraph or a section yields an identity of several hundred characters | rejected for units above the sentence |
| digest at every granularity | short identities | a stale suppression cannot be traced to its sentence without the earlier file | rejected for sentences and shorter spans |

## Consequences

- An edit of a sentence changes the identity of each finding on it, so a suppression of such a finding becomes stale and needs review. An edit elsewhere leaves the identity unchanged.
- The allowlist `terminology.terms` remains the mechanism for a class of accepted findings, such as the terms of a field. A suppression tolerates one finding.
- A rule judging a pair of sentences must name the first sentence in the evidence feature `previous_sentence_id`; otherwise its identity covers the second sentence only.
- The tests of `tests/unit/test_sarif_report.py` check each form of the discriminator and the region of a structured source. The tests of `tests/integration/test_cli_sarif.py` check the log, an incomplete run, and the refused option combinations.
