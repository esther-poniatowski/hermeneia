from __future__ import annotations

from pathlib import Path

from hermeneia.document.indexes import FeatureStore, SupportSignalKind
from hermeneia.document.markdown import MarkdownDocumentParser
from hermeneia.document.parser import ParseRequest


def test_feature_store_exposes_first_use_and_support_signals(language_pack) -> None:
    source = """The operator $T$ is defined as the transfer map.

Theorem 3 gives the key estimate.

$$
T(x)=x
$$

This clearly shows the result [Smith, 2024].
"""
    document = MarkdownDocumentParser(language_pack).parse(
        ParseRequest(source=source, path=Path("demo.md"))
    )
    features = FeatureStore(document, document.indexes)
    assert features.symbol_first_use("T") is not None
    kinds = {signal.kind for signal in document.indexes.support_signals}
    assert SupportSignalKind.THEOREM_REF in kinds
    assert SupportSignalKind.DISPLAYED_EQUATION in kinds
    assert SupportSignalKind.CITATION in kinds
    last_sentence_id = document.indexes.sentences[-1].id
    window = features.support_signals_in_window(last_sentence_id, max_sentences_back=3)
    assert any(signal.kind == SupportSignalKind.DISPLAYED_EQUATION for signal in window)
