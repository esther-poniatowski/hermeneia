from __future__ import annotations

from pathlib import Path

from hermeneia.config.profile import ProfileResolver
from hermeneia.config.schema import parse_project_config
from hermeneia.document.markdown import MarkdownDocumentParser
from hermeneia.document.parser import ParseRequest
from hermeneia.engine.runner import (
    AnalysisInput,
    AnalysisPolicy,
    AnalysisRunner,
    AnnotationResult,
)
from hermeneia.rules.base import SuggestionMode


class FlakyParser:
    def __init__(self, language_pack) -> None:
        self._delegate = MarkdownDocumentParser(language_pack)

    def parse(self, request: ParseRequest):
        if request.path and request.path.name == "bad.md":
            raise ValueError("synthetic parse failure")
        return self._delegate.parse(request)


class PassthroughAnnotator:
    def annotate(self, document, profile):  # noqa: ARG002
        return AnnotationResult(document=document)


def test_analysis_runner_continues_after_parse_failure(registry, language_pack) -> None:
    config = parse_project_config({"rules": {"active": ["surface.contraction"]}})
    profile = ProfileResolver(registry).resolve(config, language_pack)
    runner = AnalysisRunner(
        parser=FlakyParser(language_pack),
        annotator=PassthroughAnnotator(),
        registry=registry,
        language_pack=language_pack,
        embedding_backend=None,
    )
    batch = runner.analyze(
        (
            AnalysisInput(path=Path("bad.md"), source="# broken"),
            AnalysisInput(path=Path("good.md"), source="It's fine.\n"),
        ),
        profile,
    )
    assert len(batch.results) == 1
    result = batch.results[0]
    assert result.report.path == Path("good.md")
    assert any(violation.rule_id == "surface.contraction" for violation in result.violations)
    assert any(
        diagnostic.code == "parse_failure" and diagnostic.path == Path("bad.md")
        for diagnostic in batch.diagnostics
    )


def test_analysis_runner_skips_scoring_and_revision_plan_when_disabled(
    registry, language_pack
) -> None:
    config = parse_project_config({"rules": {"active": ["surface.contraction"]}})
    profile = ProfileResolver(registry).resolve(config, language_pack)
    runner = AnalysisRunner(
        parser=MarkdownDocumentParser(language_pack),
        annotator=PassthroughAnnotator(),
        registry=registry,
        language_pack=language_pack,
        embedding_backend=None,
        policy=AnalysisPolicy(
            scoring_output=frozenset({"violation_list"}),
            suggestions_enabled=False,
            suggestion_default_mode=SuggestionMode.NONE,
        ),
    )
    batch = runner.analyze(
        (AnalysisInput(path=Path("doc.md"), source="It's fine.\n"),),
        profile,
    )
    assert len(batch.results) == 1
    result = batch.results[0]
    assert result.report.scorecard is None
    assert result.report.revision_plan.operations == ()
