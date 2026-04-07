from __future__ import annotations

from pathlib import Path

from hermeneia.config.profile import ProfileResolver
from hermeneia.config.schema import parse_project_config
from hermeneia.document.indexes import FeatureStore
from hermeneia.document.markdown import MarkdownDocumentParser
from hermeneia.document.model import Document
from hermeneia.document.parser import ParseRequest
from hermeneia.engine.runner import AnalysisInput, AnalysisRunner, AnnotationResult
from hermeneia.rules.base import (
    HeuristicSemanticRule,
    Layer,
    RuleContext,
    RuleEvidence,
    RuleKind,
    RuleMetadata,
    Severity,
    Tractability,
    Violation,
)


class _PassthroughAnnotator:
    def annotate(self, document: Document, profile):  # noqa: ARG002
        return AnnotationResult(document=document)


class _ConstantEmbeddingBackend:
    def __init__(self) -> None:
        self.calls = 0

    def embed_text(self, text: str) -> tuple[float, ...]:  # noqa: ARG002
        self.calls += 1
        return (1.0, 0.0, 0.0)


class _EmbeddingRedundancyProbeRule(HeuristicSemanticRule):
    metadata = RuleMetadata(
        rule_id="test.embedding_redundancy_probe",
        label="Embedding redundancy probe",
        layer=Layer.PARAGRAPH_RHETORIC,
        tractability=Tractability.CLASS_H,
        kind=RuleKind.DIAGNOSTIC_METRIC,
        default_severity=Severity.WARNING,
        supported_languages=frozenset({"en"}),
    )

    def check(self, doc: Document, ctx: RuleContext) -> list[Violation]:
        pairs = ctx.features.redundancy_candidates(similarity_threshold=0.9)
        if not pairs:
            return []
        left_id, right_id, score = pairs[0]
        left_block = doc.block_by_id(left_id)
        if left_block is None:
            return []
        return [
            Violation(
                rule_id=self.rule_id,
                message="redundancy candidate found",
                span=left_block.span,
                severity=self.settings.severity,
                layer=self.metadata.layer,
                evidence=RuleEvidence(
                    features={"left_block_id": left_id, "right_block_id": right_id},
                    score=score,
                    threshold=0.9,
                ),
                confidence=score,
                rationale="embedding-backed redundancy candidate",
            )
        ]


def test_analysis_runner_injects_embedding_backend_for_redundancy_candidates(
    registry,
    language_pack,
) -> None:
    registry.add(_EmbeddingRedundancyProbeRule)
    config = parse_project_config(
        {"rules": {"active": [_EmbeddingRedundancyProbeRule.metadata.rule_id]}}
    )
    profile = ProfileResolver(registry).resolve(config, language_pack)
    source = "Alphaone betatwo gammathree.\n\nDeltafour epsilonfive zetasix.\n"

    runner_without_backend = AnalysisRunner(
        parser=MarkdownDocumentParser(language_pack),
        annotator=_PassthroughAnnotator(),
        registry=registry,
        language_pack=language_pack,
        embedding_backend=None,
    )
    without_backend = runner_without_backend.analyze(
        (AnalysisInput(path=Path("doc.md"), source=source),),
        profile,
    )
    assert without_backend.results
    assert without_backend.results[0].violations == ()

    embedding_backend = _ConstantEmbeddingBackend()
    runner_with_backend = AnalysisRunner(
        parser=MarkdownDocumentParser(language_pack),
        annotator=_PassthroughAnnotator(),
        registry=registry,
        language_pack=language_pack,
        embedding_backend=embedding_backend,
    )
    with_backend = runner_with_backend.analyze(
        (AnalysisInput(path=Path("doc.md"), source=source),),
        profile,
    )
    assert with_backend.results
    assert len(with_backend.results[0].violations) == 1
    assert (
        with_backend.results[0].violations[0].rule_id
        == _EmbeddingRedundancyProbeRule.metadata.rule_id
    )
    assert embedding_backend.calls >= 2


def test_redundancy_candidate_blocking_avoids_full_pairwise_scan(
    language_pack,
    monkeypatch,
) -> None:
    paragraph_count = 80
    source = "\n\n".join(f"alpha{i} beta{i} gamma{i}." for i in range(paragraph_count))
    document = MarkdownDocumentParser(language_pack).parse(
        ParseRequest(
            source=source,
            path=Path("wide.md"),
        )
    )
    features = FeatureStore(document, document.indexes)

    overlap_calls = 0
    original_overlap = FeatureStore.paragraph_overlap

    def counting_overlap(self, block_id_a: str, block_id_b: str) -> float:
        nonlocal overlap_calls
        overlap_calls += 1
        return original_overlap(self, block_id_a, block_id_b)

    monkeypatch.setattr(FeatureStore, "paragraph_overlap", counting_overlap)

    features.redundancy_candidates(similarity_threshold=0.99)
    full_pair_count = paragraph_count * (paragraph_count - 1) // 2
    assert overlap_calls < full_pair_count // 4
