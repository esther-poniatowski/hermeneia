"""Application-level analysis orchestration."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from hermeneia.document.indexes import FeatureStore
from hermeneia.document.model import Document
from hermeneia.document.parser import DocumentParser, ParseRequest
from hermeneia.engine.detector import RuleDetector
from hermeneia.engine.registry import RuleRegistry
from hermeneia.language.base import LanguagePack
from hermeneia.report.diagnostic import DiagnosticReport
from hermeneia.report.revision_plan import RevisionPlan
from hermeneia.scoring.scorer import HierarchicalScorer
from hermeneia.suggest.planner import RevisionPlanner
from hermeneia.rules.base import ResolvedProfile, Violation


@dataclass(frozen=True)
class AnalysisInput:
    path: Path | None
    source: str


@dataclass(frozen=True)
class OperationalDiagnostic:
    code: str
    message: str
    path: Path | None = None


@dataclass(frozen=True)
class AnalysisResult:
    document: Document
    profile: ResolvedProfile
    violations: tuple[Violation, ...]
    report: DiagnosticReport
    diagnostics: tuple[OperationalDiagnostic, ...] = ()


@dataclass(frozen=True)
class BatchAnalysisResult:
    results: tuple[AnalysisResult, ...]
    diagnostics: tuple[OperationalDiagnostic, ...] = ()


@dataclass(frozen=True)
class AnnotationResult:
    document: Document
    diagnostics: tuple[str, ...] = ()


class DocumentAnnotator(Protocol):
    def annotate(self, document: Document, profile: ResolvedProfile) -> AnnotationResult: ...


class AnalysisRunner:
    """Concrete orchestration for parse -> annotate -> feature -> detect -> score -> report."""

    def __init__(
        self,
        parser: DocumentParser,
        annotator: DocumentAnnotator,
        registry: RuleRegistry,
        language_pack: LanguagePack,
    ) -> None:
        self._parser = parser
        self._annotator = annotator
        self._registry = registry
        self._language_pack = language_pack
        self._detector = RuleDetector(registry)
        self._scorer = HierarchicalScorer()
        self._planner = RevisionPlanner()

    def analyze(
        self,
        inputs: tuple[AnalysisInput, ...],
        profile: ResolvedProfile,
    ) -> BatchAnalysisResult:
        results: list[AnalysisResult] = []
        diagnostics: list[OperationalDiagnostic] = []
        for analysis_input in inputs:
            parsed = self._parse_document(analysis_input, diagnostics)
            if parsed is None:
                continue
            annotation = self._annotate_document(analysis_input, profile, parsed, diagnostics)
            if annotation is None:
                continue
            features = FeatureStore(annotation.document, annotation.document.indexes)
            detection = self._detector.detect(
                annotation.document,
                profile,
                self._language_pack,
                features,
            )
            diagnostics.extend(
                OperationalDiagnostic(
                    code=diagnostic.code,
                    message=f"{diagnostic.rule_id}: {diagnostic.message}",
                    path=analysis_input.path,
                )
                for diagnostic in detection.diagnostics
            )
            scorecard = self._scorer.score(list(detection.violations))
            revision_plan = self._planner.build(list(detection.violations))
            report = DiagnosticReport(
                path=analysis_input.path,
                violations=detection.violations,
                scorecard=scorecard,
                revision_plan=revision_plan,
            )
            results.append(
                AnalysisResult(
                    document=annotation.document,
                    profile=profile,
                    violations=detection.violations,
                    report=report,
                )
            )
        return BatchAnalysisResult(results=tuple(results), diagnostics=tuple(diagnostics))

    def _parse_document(
        self,
        analysis_input: AnalysisInput,
        diagnostics: list[OperationalDiagnostic],
    ) -> Document | None:
        try:
            return self._parser.parse(
                ParseRequest(source=analysis_input.source, path=analysis_input.path)
            )
        except Exception as exc:
            diagnostics.append(
                OperationalDiagnostic(
                    code="parse_failure",
                    message=str(exc),
                    path=analysis_input.path,
                )
            )
            return None

    def _annotate_document(
        self,
        analysis_input: AnalysisInput,
        profile: ResolvedProfile,
        document: Document,
        diagnostics: list[OperationalDiagnostic],
    ) -> AnnotationResult | None:
        try:
            annotation = self._annotator.annotate(document, profile)
        except Exception as exc:
            diagnostics.append(
                OperationalDiagnostic(
                    code="annotation_failure",
                    message=str(exc),
                    path=analysis_input.path,
                )
            )
            return None
        diagnostics.extend(
            OperationalDiagnostic(
                code="annotation_backend",
                message=message,
                path=analysis_input.path,
            )
            for message in annotation.diagnostics
        )
        return annotation
