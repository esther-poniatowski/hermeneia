"""Rule dispatch over a parsed, annotated document.

Classes
-------
RuleDiagnostic
    Public API symbol.
DetectionResult
    Public API symbol.
RuleDetector
    Public API symbol.
"""

from __future__ import annotations

from dataclasses import dataclass

from hermeneia.engine.registry import RuleRegistry
from hermeneia.rules.base import (
    BaseRule,
    ResolvedProfile,
    ResolvedRuleSettings,
    RuntimeCapabilities,
    RuleContext,
    SuggestionMode,
    Tractability,
    Violation,
)
from hermeneia.document.model import Block, BlockKind, Document, Span
from hermeneia.document.indexes import FeatureStore
from hermeneia.language.base import LanguagePack

COMMA_SEPARATOR = ", "
APPLY_BLOCK_KINDS_OPTION = "apply_block_kinds"
EXCLUDE_BLOCK_KINDS_OPTION = "exclude_block_kinds"


@dataclass(frozen=True)
class RuleDiagnostic:
    """Rulediagnostic."""

    code: str
    rule_id: str
    message: str


@dataclass(frozen=True)
class DetectionResult:
    """Detectionresult."""

    violations: tuple[Violation, ...]
    diagnostics: tuple[RuleDiagnostic, ...] = ()


@dataclass(frozen=True)
class _BlockKindGate:
    """Per-rule block-kind include/exclude filters."""

    include: frozenset[BlockKind]
    exclude: frozenset[BlockKind]


class RuleDetector:
    """Ruledetector.

    Parameters
    ----------
    registry : RuleRegistry
        Rule registry used to resolve implementations.
    """

    def __init__(self, registry: RuleRegistry) -> None:
        """Initialize the instance."""
        self._registry = registry

    def detect(
        self,
        document: Document,
        profile: ResolvedProfile,
        language_pack: LanguagePack,
        features: FeatureStore,
        debug_mode: bool = False,
    ) -> DetectionResult:
        """Detect.

        Parameters
        ----------
        document : Document
            Document instance to inspect.
        profile : ResolvedProfile
            Resolved profile controlling rule behavior.
        language_pack : LanguagePack
            Input value for ``language_pack``.
        features : FeatureStore
            Input value for ``features``.
        debug_mode : bool
            Input value for ``debug_mode``.

        Returns
        -------
        DetectionResult
            Resulting value produced by this call.
        """
        context = RuleContext(
            profile=profile,
            language_pack=language_pack,
            features=features,
            capabilities=RuntimeCapabilities(
                embeddings_available=features.embeddings_available,
                debug_mode=debug_mode,
                experimental_rules_enabled=profile.enable_experimental,
            ),
        )
        violations: list[Violation] = []
        diagnostics: list[RuleDiagnostic] = []
        # Defensive boundary: rule modules are extension points.
        # pylint: disable=broad-exception-caught
        for settings in profile.active_rules():
            try:
                rule = self._registry.instantiate(settings)
            except Exception as exc:  # pragma: no cover
                diagnostics.append(
                    RuleDiagnostic(
                        code="rule_instantiation_error",
                        rule_id=settings.metadata.rule_id,
                        message=str(exc),
                    )
                )
                continue
            try:
                rule_violations = rule.check(document, context)
            except Exception as exc:
                diagnostics.append(
                    RuleDiagnostic(
                        code="rule_execution_error",
                        rule_id=rule.rule_id,
                        message=str(exc),
                    )
                )
                continue
            try:
                rule_violations = _apply_block_kind_gate(
                    rule_violations,
                    settings,
                    document,
                )
            except ValueError as exc:
                diagnostics.append(
                    RuleDiagnostic(
                        code="rule_options_error",
                        rule_id=rule.rule_id,
                        message=str(exc),
                    )
                )
                continue
            for violation in rule_violations:
                issue = _validate_violation_contract(rule, violation)
                if issue is not None:
                    diagnostics.append(
                        RuleDiagnostic(
                            code="rule_contract_error",
                            rule_id=rule.rule_id,
                            message=issue,
                        )
                    )
                    continue
                violations.append(violation)
        ordered_violations = tuple(
            sorted(
                violations,
                key=lambda violation: (violation.span.start, violation.rule_id),
            )
        )
        return DetectionResult(
            violations=ordered_violations, diagnostics=tuple(diagnostics)
        )


def _validate_violation_contract(rule: BaseRule, violation: Violation) -> str | None:
    """Validate violation contract."""
    metadata = rule.metadata
    if violation.rule_id != metadata.rule_id:
        return (
            f"violation rule_id '{violation.rule_id}' does not match metadata id "
            f"'{metadata.rule_id}'"
        )
    if violation.layer != metadata.layer:
        return (
            f"violation layer '{violation.layer.value}' does not match metadata layer "
            f"'{metadata.layer.value}'"
        )
    if metadata.evidence_fields:
        if violation.evidence is None:
            return "violation is missing evidence required by rule metadata"
        missing = [
            field
            for field in metadata.evidence_fields
            if field not in violation.evidence.features
        ]
        if missing:
            return (
                "violation evidence is missing required fields: "
                f"{COMMA_SEPARATOR.join(missing)}"
            )
    if metadata.tractability == Tractability.CLASS_H:
        if violation.evidence is None:
            return "class_h violation must include evidence"
        if violation.confidence is None:
            return "class_h violation must include confidence"
    if violation.confidence is not None and not 0.0 <= violation.confidence <= 1.0:
        return "violation confidence must be between 0.0 and 1.0"
    if metadata.suggestion_mode == SuggestionMode.NONE and violation.rewrite_tactics:
        return "rule with suggestion_mode='none' emitted rewrite tactics"
    return None


def _apply_block_kind_gate(
    violations: list[Violation],
    settings: ResolvedRuleSettings,
    document: Document,
) -> list[Violation]:
    """Apply block-kind include/exclude filtering to rule output."""
    gate = _resolve_block_kind_gate(settings)
    if not gate.include and not gate.exclude:
        return violations
    blocks_by_span_size = sorted(
        document.iter_blocks(),
        key=lambda block: (block.span.end - block.span.start, block.span.start),
    )
    span_kind_cache: dict[tuple[int, int], BlockKind | None] = {}
    filtered: list[Violation] = []
    for violation in violations:
        cache_key = (violation.span.start, violation.span.end)
        if cache_key not in span_kind_cache:
            span_kind_cache[cache_key] = _block_kind_for_span(
                violation.span,
                blocks_by_span_size,
            )
        block_kind = span_kind_cache[cache_key]
        if _block_kind_allowed(block_kind, gate):
            filtered.append(violation)
    return filtered


def _resolve_block_kind_gate(settings: ResolvedRuleSettings) -> _BlockKindGate:
    """Resolve block-kind gate options from rule settings."""
    include = _coerce_block_kind_set(
        settings.options.get(APPLY_BLOCK_KINDS_OPTION, ()),
        field_name=APPLY_BLOCK_KINDS_OPTION,
    )
    exclude = _coerce_block_kind_set(
        settings.options.get(EXCLUDE_BLOCK_KINDS_OPTION, ()),
        field_name=EXCLUDE_BLOCK_KINDS_OPTION,
    )
    return _BlockKindGate(include=include, exclude=exclude)


def _coerce_block_kind_set(raw: object, *, field_name: str) -> frozenset[BlockKind]:
    """Coerce a raw block-kind option value into enum members."""
    if raw is None:
        return frozenset()
    if not isinstance(raw, (list, tuple, set, frozenset)):
        raise ValueError(f"{field_name} must be a sequence of block kind names")
    values: set[BlockKind] = set()
    for item in raw:
        if isinstance(item, BlockKind):
            values.add(item)
            continue
        if not isinstance(item, str):
            raise ValueError(f"{field_name} must contain only block kind names")
        try:
            values.add(BlockKind(item.strip().lower()))
        except ValueError as exc:
            expected = ", ".join(sorted(kind.value for kind in BlockKind))
            raise ValueError(
                f"{field_name} includes unknown block kind '{item}'. "
                f"Expected one of: {expected}"
            ) from exc
    return frozenset(values)


def _block_kind_for_span(span: Span, blocks: list[Block]) -> BlockKind | None:
    """Find the most specific block kind that contains the span."""
    for block in blocks:
        if span.start < block.span.start:
            continue
        if span.end > block.span.end:
            continue
        return block.kind
    return None


def _block_kind_allowed(block_kind: BlockKind | None, gate: _BlockKindGate) -> bool:
    """Check whether a block kind passes include/exclude gate constraints."""
    if gate.include:
        if block_kind is None or block_kind not in gate.include:
            return False
    if block_kind is not None and block_kind in gate.exclude:
        return False
    return True
