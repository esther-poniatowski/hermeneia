"""Write analysis results as a log of the findings profile of Elenchos, a subset of SARIF 2.1.0.

The log holds one run of the driver ``hermeneia``, whose driver lists every registered rule. Each
result names its rule, its level and its message, the analysed file as a physical location
relative to ``SRCROOT`` with the region of the violation, and one logical location
``path:<file>``. The gate builds the identity of each result from the tool, the rule, the resource
and the discriminator, and writes the suppressions; a producer writes neither.

A violation has no locus that survives edits: its offsets and its sentence identifiers shift when
text is inserted earlier in the file. The locus is therefore empty, and the discriminator holds the
text that the rule judged, so that the identity changes exactly when that text changes:

- a violation on one sentence takes the normalized sentence;
- a violation on part of a sentence takes the matched words in brackets, then the sentence;
- a violation on a pair of sentences, a block, a section or source lines takes a digest of the
  normalized text, since that text may run to several hundred characters.

Every operational diagnostic of the batch, such as a file that could not be parsed or a rule that
failed, means that some rule was not evaluated on some file. The run then declares itself failed,
with one notification of level ``error`` per diagnostic, and keeps the results detected.
"""

from __future__ import annotations

import hashlib
import re
import unicodedata
from collections.abc import Iterable, Sequence
from pathlib import Path
from typing import Any
from urllib.parse import quote

from hermeneia.document.model import Document, SourceKind, Span
from hermeneia.engine.registry import RuleRegistration
from hermeneia.engine.runner import BatchAnalysisResult, OperationalDiagnostic
from hermeneia.rules.base import Severity, Violation

SARIF_VERSION = "2.1.0"
SARIF_SCHEMA = (
    "https://docs.oasis-open.org/sarif/sarif/v2.1.0/errata01/os/schemas/sarif-schema-2.1.0.json"
)
TOOL_NAME = "hermeneia"
URI_BASE_ID = "SRCROOT"
DISCRIMINATOR_KEY = "discriminator/v1"
DIGEST_PREFIX = "sha256:"
DIGEST_LENGTH = 16
"""Hexadecimal digits kept from the digest: 64 bits, enough to separate the units of one file."""

LEVELS = {Severity.ERROR: "error", Severity.WARNING: "warning", Severity.INFO: "note"}
"""SARIF has no level ``info``; the profile maps it to ``note``."""

#: The evidence feature naming the first sentence of a pair, set by the rules judging pairs.
PREVIOUS_SENTENCE_FEATURE = "previous_sentence_id"

# The characters of an RFC 3986 path segment kept as written, besides unreserved characters: the
# sub-delimiters and ``@``. A colon is encoded, so that a first segment never reads as a scheme.
_URI_SAFE = "/!$&'()*+,;=@"
_WHITESPACE = re.compile(r"\s+")


def normalize(text: str) -> str:
    """Return ``text`` in NFC, with each run of whitespace collapsed to one space and trimmed."""
    return _WHITESPACE.sub(" ", unicodedata.normalize("NFC", text)).strip()


def digest(text: str) -> str:
    """Return the prefixed digest of the normalized ``text``."""
    value = hashlib.sha256(normalize(text).encode("utf-8")).hexdigest()
    return DIGEST_PREFIX + value[:DIGEST_LENGTH]


def _contains(outer: Span, inner: Span) -> bool:
    """Return whether the offsets of ``inner`` lie within those of ``outer``."""
    return outer.start <= inner.start and inner.end <= outer.end


def discriminator(document: Document, violation: Violation) -> str:
    """Return the discriminator of ``violation``: the text that its rule judged.

    The sentence holding the span decides the form. A span equal to that sentence yields the
    sentence, and a shorter span yields the matched words in brackets followed by the sentence. A
    span on the second sentence of a pair, named by the evidence of the violation, yields the
    digest of both sentences. A span that no sentence holds yields the digest of its text, and an
    empty span yields the empty string, so the gate numbers identical occurrences.
    """
    source = document.source
    span = violation.span
    text = normalize(source[span.start : span.end])
    if not text:
        return ""
    sentence = next(
        (
            sentence
            for block in document.iter_blocks()
            for sentence in block.sentences
            if _contains(sentence.span, span)
        ),
        None,
    )
    if sentence is None:
        return digest(text)
    whole = normalize(source[sentence.span.start : sentence.span.end])
    features = violation.evidence.features if violation.evidence is not None else {}
    previous_id = features.get(PREVIOUS_SENTENCE_FEATURE)
    previous = document.sentence_by_id(previous_id) if isinstance(previous_id, str) else None
    if previous is not None:
        first = source[previous.span.start : previous.span.end]
        return digest(f"{first} {whole}")
    if text == whole:
        return whole
    return f"[{text}] {whole}"


def relative_path(path: Path, root: Path) -> str:
    """Return the POSIX path of ``path`` relative to ``root``; raise when it lies outside."""
    resolved = path.resolve()
    if not resolved.is_relative_to(root.resolve()):
        raise ValueError(f"{path} lies outside the root {root}")
    return resolved.relative_to(root.resolve()).as_posix()


def logical_name(relative: str) -> str:
    """Return ``path:<path>``, with ``%`` written ``%25`` and ``#`` written ``%23``."""
    return "path:" + relative.replace("%", "%25").replace("#", "%23")


def artifact_uri(relative: str) -> str:
    """Return the relative path percent-encoded as a relative URI reference."""
    return quote(relative, safe=_URI_SAFE)


def region(document: Document, span: Span) -> dict[str, int]:
    """Return the region of ``span``, its lines located in the source file.

    The columns of a structured source count positions in its Markdown projection, not in the
    file, so its region holds lines only.
    """
    located: dict[str, int] = {
        "startLine": document.source_line(span.start_line),
        "endLine": document.source_line(span.end_line),
    }
    if document.source_kind == SourceKind.MARKDOWN:
        located["startColumn"] = span.start_column
        located["endColumn"] = span.end_column
    return located


def _properties(violation: Violation) -> dict[str, Any]:
    """Return the payload of Hermeneia for a result, each name prefixed by the driver name."""
    properties: dict[str, Any] = {"hermeneia/layer": violation.layer.value}
    if violation.confidence is not None:
        properties["hermeneia/confidence"] = violation.confidence
    if violation.rationale:
        properties["hermeneia/rationale"] = violation.rationale
    if violation.rewrite_tactics:
        properties["hermeneia/rewrite_tactics"] = list(violation.rewrite_tactics)
    evidence = violation.evidence
    if evidence is not None:
        properties["hermeneia/evidence"] = {
            "score": evidence.score,
            "threshold": evidence.threshold,
            "features": dict(evidence.features),
        }
    return properties


def _result(document: Document, violation: Violation, relative: str) -> dict[str, Any]:
    """Return the SARIF result of ``violation``, found in the file at ``relative``."""
    result: dict[str, Any] = {
        "ruleId": violation.rule_id,
        "level": LEVELS[violation.severity],
        "message": {"text": violation.message},
        "locations": [
            {
                "physicalLocation": {
                    "artifactLocation": {"uri": artifact_uri(relative), "uriBaseId": URI_BASE_ID},
                    "region": region(document, violation.span),
                },
                "logicalLocations": [{"name": logical_name(relative)}],
            }
        ],
        "properties": _properties(violation),
    }
    key = discriminator(document, violation)
    if key:
        result["partialFingerprints"] = {DISCRIMINATOR_KEY: key}
    return result


def _notification(diagnostic: OperationalDiagnostic, root: Path) -> dict[str, Any]:
    """Return the error notification stating why ``diagnostic`` left a rule unevaluated."""
    location = ""
    if diagnostic.path is not None:
        location = f"{relative_path(diagnostic.path, root)}: "
    return {
        "level": "error",
        "message": {"text": f"{location}{diagnostic.code}: {diagnostic.message}"},
    }


def _invocation(diagnostics: Sequence[OperationalDiagnostic], root: Path) -> dict[str, Any]:
    """Return the invocation of the run, failed when any operational diagnostic arose."""
    if not diagnostics:
        return {"executionSuccessful": True}
    return {
        "executionSuccessful": False,
        "toolExecutionNotifications": [_notification(item, root) for item in diagnostics],
    }


def sarif_log(
    batch: BatchAnalysisResult,
    rules: Iterable[RuleRegistration],
    version: str,
    root: Path,
) -> dict[str, Any]:
    """Return the log of one run of Hermeneia of ``version``, with paths relative to ``root``.

    ``rules`` lists every rule that the run can emit, whether or not the profile activates it.
    Every result of ``batch`` must come from a file under ``root``.
    """
    results: list[dict[str, Any]] = []
    diagnostics = [*batch.diagnostics]
    for analysis in batch.results:
        diagnostics.extend(analysis.diagnostics)
        if analysis.report.path is None:
            raise ValueError("a findings log requires every analysed source to be a file")
        relative = relative_path(analysis.report.path, root)
        results.extend(
            _result(analysis.document, violation, relative) for violation in analysis.violations
        )
    descriptors = [
        {
            "id": registration.metadata.rule_id,
            "shortDescription": {"text": registration.metadata.label},
            "defaultConfiguration": {"level": LEVELS[registration.metadata.default_severity]},
        }
        for registration in sorted(rules, key=lambda item: item.metadata.rule_id)
    ]
    return {
        "version": SARIF_VERSION,
        "$schema": SARIF_SCHEMA,
        "runs": [
            {
                "tool": {"driver": {"name": TOOL_NAME, "version": version, "rules": descriptors}},
                "invocations": [_invocation(diagnostics, root)],
                "columnKind": "unicodeCodePoints",
                "results": results,
            }
        ],
    }
