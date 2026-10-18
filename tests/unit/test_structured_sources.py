"""Tests of the structured sources: their projection, the form of their strings, and their scope.

A YAML file, a Python module and a commit message are projected to Markdown before analysis. The
tests check that each string becomes one paragraph located in its source, that the field-form rule
reads the kind of each string, and that the rules reading paragraphs and sections do not
apply to a structured source.
"""

from __future__ import annotations

from pathlib import Path

from hermeneia.document.annotator import SpaCyDocumentAnnotator
from hermeneia.document.indexes import FeatureStore
from hermeneia.document.markdown import MarkdownDocumentParser
from hermeneia.document.model import FieldKind, SourceKind
from hermeneia.document.parser import ParseRequest
from hermeneia.document.structured import project
from hermeneia.rules.base import RuleContext

YAML = """\
# settings of the checkers; one block
# continued on a second line
skip:
  code:
    gloss: inline code and fenced blocks
  math:
    gloss: The masked spans of mathematics.
  # Capitalized comment, closed by a period.
  links:
    gloss: the target of a link, whose text stays scanned
template:
  holds: EXPRESSION OVER DECLARED SYMBOLS
rationale: "The checker reads the value. It reports a mismatch."
name: the link checker.
"""

PYTHON = '''\
"""Read the declared kinds of a checker.

Parameters
----------
path : Path
    File holding the declarations.

Examples
--------
>>> read(Path("a"))
"""

# the kinds are read once, at import
KINDS = ()  # noqa: E501
'''

COMMIT = """\
Add the checker tests.

The suite runs before each commit that changes a checker.

Co-Authored-By: Someone <someone@example.org>
# Please enter the commit message for your changes.
"""


def _check(kind, source, rule_id, registry, language_pack, research_profile):
    """Project a source, run one rule on it, and return the source lines of its findings."""
    projection = project(kind, source)
    document = MarkdownDocumentParser(language_pack).parse(
        ParseRequest(
            source=projection.markdown,
            path=Path("source"),
            source_kind=kind,
            fields=projection.fields,
            line_map=projection.line_map,
        )
    )
    document = (
        SpaCyDocumentAnnotator(language_pack.parser_model)
        .annotate(document, research_profile)
        .document
    )
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules[rule_id])
    return sorted(document.source_line(v.span.start_line) for v in rule.check(document, context))


def test_yaml_projection_keeps_one_paragraph_per_string() -> None:
    projection = project(SourceKind.YAML, YAML)
    kinds = [(item.kind, item.source_line) for item in projection.fields]
    assert (FieldKind.COMMENT, 1) in kinds  # the two comment lines form one string
    assert (FieldKind.COMMENT, 2) not in kinds
    assert (FieldKind.LABEL, 14) in kinds
    assert all(projection.line_map[item.line - 1] == item.source_line for item in projection.fields)


def test_python_projection_keeps_prose_only() -> None:
    texts = [item.text for item in project(SourceKind.PYTHON, PYTHON).fields]
    assert texts == [
        "Read the declared kinds of a checker.",
        "File holding the declarations.",
        "the kinds are read once, at import",
    ]


def test_commit_projection_skips_trailers_and_comments() -> None:
    fields = project(SourceKind.COMMIT, COMMIT).fields
    assert [item.kind for item in fields] == [FieldKind.COMMIT_SUBJECT, FieldKind.COMMIT_BODY]


def test_field_form_reports_each_kind_against_its_form(
    registry, language_pack, research_profile
) -> None:
    lines = _check(
        SourceKind.YAML, YAML, "structure.field_form", registry, language_pack, research_profile
    )
    # the capitalized gloss, the capitalized comment, the template value and the label period fail;
    # the lowercase comment block, the lowercase glosses and the paragraph value pass
    assert lines == [7, 8, 12, 14]


def test_field_form_reads_a_commit_subject_as_a_label(
    registry, language_pack, research_profile
) -> None:
    lines = _check(
        SourceKind.COMMIT, COMMIT, "structure.field_form", registry, language_pack, research_profile
    )
    assert lines == [1]


def test_paragraph_rules_leave_structured_sources_alone(
    registry, language_pack, research_profile
) -> None:
    from hermeneia.engine.detector import RuleDetector

    projection = project(SourceKind.YAML, YAML)
    document = MarkdownDocumentParser(language_pack).parse(
        ParseRequest(
            source=projection.markdown,
            source_kind=SourceKind.YAML,
            fields=projection.fields,
            line_map=projection.line_map,
        )
    )
    document = (
        SpaCyDocumentAnnotator(language_pack.parser_model)
        .annotate(document, research_profile)
        .document
    )
    detection = RuleDetector(registry).detect(
        document, research_profile, language_pack, FeatureStore(document, document.indexes)
    )
    layers = {
        registry.instantiate(research_profile.rules[v.rule_id]).metadata.layer.value
        for v in detection.violations
    }
    assert layers <= {"surface_style", "local_discourse"}


NOTE = """\
---
role: note
purpose: "fixes the settings read by the checkers."
contribution:
  - the gain decays as the variance grows
  - The bound holds for every gain
title: Not projected
---
# Note
"""


def test_frontmatter_projection_keeps_the_selected_keys_on_their_lines() -> None:
    from hermeneia.document.structured import project_frontmatter

    fields = project_frontmatter(NOTE, frozenset({"purpose", "contribution"})).fields
    assert [(item.key, item.source_line) for item in fields] == [
        ("purpose", 3),
        ("contribution", 5),
        ("contribution", 6),
    ]


def test_declared_forms_outrank_the_inferred_form(registry, language_pack) -> None:
    from hermeneia.config.profile import ProfileResolver
    from hermeneia.config.schema import parse_project_config
    from hermeneia.document.structured import project_frontmatter

    config = parse_project_config(
        {
            "rules": {
                "overrides": {
                    "structure.field_form": {
                        "options": {"forms": {"purpose": "gloss", "contribution": "gloss"}}
                    }
                }
            }
        }
    )
    profile = ProfileResolver(registry).resolve(config, language_pack)
    projection = project_frontmatter(NOTE, frozenset({"purpose", "contribution"}))
    document = MarkdownDocumentParser(language_pack).parse(
        ParseRequest(
            source=projection.markdown,
            source_kind=SourceKind.YAML,
            fields=projection.fields,
            line_map=projection.line_map,
        )
    )
    document = (
        SpaCyDocumentAnnotator(language_pack.parser_model).annotate(document, profile).document
    )
    context = RuleContext(profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(profile.rules["structure.field_form"])
    lines = sorted(document.source_line(v.span.start_line) for v in rule.check(document, context))
    # the purpose closes on a period and the second contribution opens on a capital; the first
    # contribution, a lowercase clause with a subject, passes as a declared entry
    assert lines == [3, 6]
