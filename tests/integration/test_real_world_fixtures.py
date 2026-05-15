from __future__ import annotations

from pathlib import Path
from typing import Any

from hermeneia.config.profile import ProfileResolver
from hermeneia.config.schema import parse_project_config
from hermeneia.document.annotator import SpaCyDocumentAnnotator
from hermeneia.document.markdown import MarkdownDocumentParser
from hermeneia.engine.runner import AnalysisInput, AnalysisResult, AnalysisRunner

FIXTURE_ROOT = Path(__file__).resolve().parents[1] / "fixtures" / "real_world"


def _analyze_fixture(
    fixture_name: str,
    config_data: dict[str, Any],
    registry,
    language_pack,
) -> tuple[str, AnalysisResult]:
    fixture_path = FIXTURE_ROOT / fixture_name
    source = fixture_path.read_text(encoding="utf-8")
    profile = ProfileResolver(registry).resolve(parse_project_config(config_data), language_pack)
    runner = AnalysisRunner(
        parser=MarkdownDocumentParser(language_pack),
        annotator=SpaCyDocumentAnnotator(language_pack.parser_model),
        registry=registry,
        language_pack=language_pack,
        embedding_backend=None,
    )
    batch = runner.analyze((AnalysisInput(path=fixture_path, source=source),), profile)
    assert batch.diagnostics == ()
    assert len(batch.results) == 1
    return source, batch.results[0]


def test_plan_style_fixture_locks_false_alarm_tuning(registry, language_pack) -> None:
    _source, result = _analyze_fixture(
        "plan_style.md",
        {
            "rules": {
                "active": [
                    "terminology.acronym_burden",
                    "linkage.transition_quality",
                    "syntax.sentence_length",
                ],
                "overrides": {
                    "syntax.sentence_length": {"options": {"max_words": 8}},
                    "linkage.transition_quality": {
                        "options": {
                            "max_shift_findings": 0,
                            "min_paragraph_sentences": 99,
                            "detect_if_without_then": True,
                            "max_if_without_then_findings": 10,
                            "detect_implicit_contrast": True,
                            "max_implicit_contrast_findings": 10,
                            "min_overlap_for_implicit_contrast": 1.1,
                        }
                    },
                },
            }
        },
        registry,
        language_pack,
    )
    assert not any(
        violation.rule_id == "terminology.acronym_burden" for violation in result.violations
    )

    transition_issues = [
        str(violation.evidence.features.get("issue"))
        for violation in result.violations
        if violation.rule_id == "linkage.transition_quality" and violation.evidence is not None
    ]
    assert transition_issues.count("if_consequence_without_then") == 1
    assert transition_issues.count("implicit_contrast_without_marker") == 1

    sentence_by_span = {
        (sentence.span.start, sentence.span.end): sentence
        for block in result.document.iter_blocks()
        for sentence in block.sentences
    }
    length_violations = [
        violation
        for violation in result.violations
        if violation.rule_id == "syntax.sentence_length"
    ]
    assert len(length_violations) >= 3
    matched_sentences = [
        sentence_by_span[(violation.span.start, violation.span.end)]
        for violation in length_violations
    ]
    assert any("table_cell_context" in sentence.annotation_flags for sentence in matched_sentences)
    assert any("blockquote_context" in sentence.annotation_flags for sentence in matched_sentences)
    assert all("[!NOTE]" not in sentence.source_text for sentence in matched_sentences)

    table_cell_sentences = [
        sentence.source_text
        for sentence in sentence_by_span.values()
        if "table_cell_context" in sentence.annotation_flags
    ]
    assert any(
        text.startswith("The preparation sequence defines baseline inputs")
        for text in table_cell_sentences
    )
    assert any(
        text.startswith("The evaluation branch tracks error signals")
        for text in table_cell_sentences
    )


def test_handoff_style_fixture_locks_rule_mix(registry, language_pack) -> None:
    _source, result = _analyze_fixture(
        "handoff_style.md",
        {
            "rules": {
                "active": [
                    "structure.declarative_heading",
                    "reference.structural_metalanguage",
                    "reference.citation_as_agent",
                    "reference.citation_tail_parenthetical",
                    "vocabulary.filler_noun_scaffolding",
                    "vocabulary.cardinality_framing",
                ]
            }
        },
        registry,
        language_pack,
    )
    observed_rule_ids = {violation.rule_id for violation in result.violations}
    expected_rule_ids = {
        "structure.declarative_heading",
        "reference.structural_metalanguage",
        "reference.citation_as_agent",
        "reference.citation_tail_parenthetical",
        "vocabulary.filler_noun_scaffolding",
        "vocabulary.cardinality_framing",
    }
    assert expected_rule_ids.issubset(observed_rule_ids)
