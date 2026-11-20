# Boundary with the geonexus checkers

Two rules fix the [boundary between hermeneia and geonexus](../adr/0008-geonexus-boundary.md): hermeneia owns sentence-level prose, and geonexus implements no checker that could carry a concern of hermeneia. The kinds of finding reported by the geonexus checkers are each assigned below to one side of that boundary. When a kind belongs to hermeneia, geonexus can retire it only once hermeneia carries the same check. Therefore, the changes required in hermeneia are listed beside each such kind.

## Baseline and criterion

The checkers were read at geonexus commit `b32ed7d5`, in `utils/scripts/`. Each module lists its kinds of finding in its docstring.

Each kind is assigned by the criterion of the boundary decision. Under that criterion, a check belongs to hermeneia when it reads the wording or the form of a prose string. A check stays with geonexus when it reads the structural data of the vault.

## Kinds that hermeneia must carry

| Kind | Checker | Test | hermeneia counterpart | Missing in hermeneia |
| --- | --- | --- | --- | --- |
| `purpose-frame`, `contribution-frame` | `check_frontmatter.py`, through the class `Frame` of `index_entries/fields.py` | one sentence, lowercase opening, no final period, and no opening among the forbidden openings declared per key in `specs/vocabulary/keys.yml` | `structure.field_form`, form `gloss` | the test for one sentence; forbidden openings per key |
| `invalid-cites`, for a `for` value breaking its frame | `check_frontmatter.py` | the same frame, applied to the `for` value of a citation entry | `structure.field_form`, form `gloss` | the same two tests; the reading of a value nested in a list of entries |
| `gloss-form`, `gloss-opening` | `check_glossary.py`, through `glossary_checks/gloss.py` | one sentence on one line, lowercase opening, no final period; an acronym, a formula and a declared proper noun may open a gloss | `structure.field_form`, form `gloss` | the three exceptions to the lowercase opening |
| `schema-violation`, when raised by the pattern `$defs.gloss` | `check_glossary.py`, through `utils/schemas/glossary.schema.yaml` | a regular expression rejecting a second sentence and a final period | `structure.field_form`, form `gloss` | none beyond the rows above |

The pattern `$defs.gloss` must be reduced to its structural part, a string on one line, once hermeneia carries the form.

## Kinds whose owner is undecided

Three groups of kinds read the words or the links of a note, but depend on data resolved by geonexus alone. Each group needs a decision.

### Terms bound by a glossary

Four kinds compare the words of a note with the glossary and the audiences bound to that note:

- `forbidden-term`;
- `deprecated-term`;
- `candidate-term`;
- `frame-mismatch`.

These words are sentence-level prose, so the criterion assigns the four kinds to hermeneia. However, geonexus alone resolves the binding of a note. The binding is resolved through three declarations, from the frontmatter of the note up to the nearest specification of its folder. When resolving the binding, geonexus also merges the imports between glossaries. hermeneia reads the labels of a glossary through `terminology.files`, but represents no forbidden, deprecated or candidate term. One option keeps the resolution in geonexus: geonexus writes the terms bound to each note to a file, and hermeneia reads that file.

### Symbols bound by a notation file

Four kinds compare the symbols of a math span with a notation file:

- `deprecated-symbol`;
- `candidate-symbol`;
- `conflicting-symbol`;
- the report of a symbol missing from the notation file.

A symbol belongs to notation rather than to a sentence. However, the `math.*` rules of hermeneia already check notation in prose, so the criterion does not settle the owner of these kinds.

### Fragments of a link

`heading-fragment` reports a link whose fragment is a heading slug instead of a block anchor. `reference.heading_link` of hermeneia checks the same form in the body of a Markdown note. The form of a link belongs to the structural data of the vault, so the criterion assigns the check to geonexus. `check_links.py` also applies the check to the `source` values of YAML files, whereas hermeneia does not read those values as prose. Two checkers of one form must not coexist. Either geonexus keeps the kind and hermeneia retires its rule for the projects that run a link checker, or geonexus retires the kind.

## Kinds outside the concerns of hermeneia

Each remaining kind reads the structural data of the vault, so it stays with geonexus:

| Checker | Kinds that stay with geonexus |
| --- | --- |
| `check_frontmatter.py` | every kind, except `purpose-frame`, `contribution-frame` and the frame of a `for` value in `invalid-cites` |
| `check_links.py` | `broken`, `convention`, `broken-anchor` and `foreign-scheme`; `heading-fragment` awaits its decision |
| `check_glossary.py` | every kind, except `gloss-form`, `gloss-opening` and the pattern `$defs.gloss`; the kinds of terms and symbols await their decisions |
| `check_structure.py`, `check_tasks.py`, `check_manifests.py`, `check_dependencies.py`, `check_palette.py`, `check_baseline.py` | every kind |

## Consequences for geonexus

Three parts of geonexus change when the kinds of the first table move to hermeneia:

- **Gating.** The validation rules of geonexus, in `docs/rules/validation.md`, keep hermeneia out of the commit gate. Therefore, the moved kinds leave the gate, unless the gate runs hermeneia. `check_baseline.py` runs any command declared under `baselines` in `config/checks.yaml`. Consequently, the gate keeps the moved kinds once `config/checks.yaml` declares `hermeneia lint --rule structure.field_form`, with a baseline of its own.
- **Data.** The forbidden openings of each key are declared in `specs/vocabulary/keys.yml`. Under the geonexus rule "declare each checkable rule once, in data read by the checker", they must move to the `.hermeneia.yaml` of the vault and leave `keys.yml`.
- **Configuration.** The `.hermeneia.yaml` of the vault declares 26 nouns as project terms to silence `vocabulary.nominalization`. That list can be removed once the nominalization rule reports only an event reading, as proposed in the [resolution of the nominalization conflict](oikos-style-conflicts.md).
