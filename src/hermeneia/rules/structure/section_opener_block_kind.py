"""Section-opener block-kind and framing checks."""

from __future__ import annotations

from hermeneia.document.model import BlockKind
from hermeneia.rules.base import (
    HeuristicSemanticRule,
    Layer,
    RuleEvidence,
    RuleKind,
    RuleMetadata,
    Severity,
    Tractability,
    Violation,
)
from hermeneia.rules.patterns import compile_leading_phrase_regex
from hermeneia.rules.structure._option_parsing import (
    as_block_kind_name_tuple,
    mapping_with_allowed_keys,
    resolve_block_kinds,
)

DEFAULT_BLOCKED_OPENING_KINDS = (
    BlockKind.DISPLAY_MATH,
    BlockKind.CODE_BLOCK,
    BlockKind.LIST,
    BlockKind.TABLE,
)


class _SectionOpenerBlockKindOptions:
    def __init__(
        self,
        *,
        blocked_block_kinds: tuple[str, ...] | None = None,
        apply_heading_levels: tuple[int, ...] | None = None,
    ) -> None:
        self.blocked_block_kinds = blocked_block_kinds
        self.apply_heading_levels = apply_heading_levels

    @classmethod
    def model_validate(cls, raw: object) -> "_SectionOpenerBlockKindOptions":
        mapping = mapping_with_allowed_keys(
            raw,
            allowed=frozenset({"blocked_block_kinds", "apply_heading_levels"}),
            scope="section_opener_block_kind options",
        )
        blocked_block_kinds = as_block_kind_name_tuple(
            mapping.get("blocked_block_kinds"), field="blocked_block_kinds"
        )
        apply_heading_levels = _parse_heading_levels(mapping.get("apply_heading_levels"))
        return cls(
            blocked_block_kinds=blocked_block_kinds,
            apply_heading_levels=apply_heading_levels,
        )

    def model_dump(self) -> dict[str, object]:
        dumped: dict[str, object] = {}
        if self.blocked_block_kinds is not None:
            dumped["blocked_block_kinds"] = self.blocked_block_kinds
        if self.apply_heading_levels is not None:
            dumped["apply_heading_levels"] = self.apply_heading_levels
        return dumped


class SectionOpenerBlockKindRule(HeuristicSemanticRule):
    options_model = _SectionOpenerBlockKindOptions

    metadata = RuleMetadata(
        rule_id="structure.section_opener_block_kind",
        label="Section should open with purpose-oriented prose",
        layer=Layer.DOCUMENT_STRUCTURE,
        tractability=Tractability.CLASS_H,
        kind=RuleKind.RHETORICAL_EXPECTATION,
        default_severity=Severity.INFO,
        supported_languages=frozenset({"en"}),
        default_options={
            "blocked_block_kinds": tuple(kind.value for kind in DEFAULT_BLOCKED_OPENING_KINDS),
        },
        evidence_fields=("issue", "first_block_kind"),
    )

    def check(self, doc, ctx):
        blocked_opening_kinds = resolve_block_kinds(
            self.settings.options.get("blocked_block_kinds"),
            field="blocked_block_kinds",
            default=DEFAULT_BLOCKED_OPENING_KINDS,
        )
        apply_levels = _resolve_heading_levels(self.settings.options.get("apply_heading_levels"))
        definition_openers = tuple(ctx.language_pack.lexicons.definitional_markers) + (
            "definition",
        )
        definition_pattern = compile_leading_phrase_regex(definition_openers)
        violations: list[Violation] = []
        for section in ctx.features.sections:
            if section.heading_block_id is None or len(section.block_ids) < 2:
                continue
            if apply_levels is not None and section.level not in apply_levels:
                continue
            first_content = doc.block_by_id(section.block_ids[1])
            heading = doc.block_by_id(section.heading_block_id)
            if first_content is None or heading is None:
                continue
            issue = _section_opening_issue(
                first_content,
                definition_pattern=definition_pattern,
                blocked_opening_kinds=blocked_opening_kinds,
            )
            if issue is None:
                continue
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    message=(
                        "Section opens without purpose-oriented prose; introduce the section "
                        "question or strategy before raw structured blocks or definitional framing."
                    ),
                    span=first_content.span,
                    severity=self.settings.severity,
                    layer=self.metadata.layer,
                    evidence=RuleEvidence(
                        features={
                            "issue": issue,
                            "section_heading_id": heading.id,
                            "first_block_kind": first_content.kind.value,
                        }
                    ),
                    confidence=0.72,
                    rationale=(
                        "Section-opener checks inspect only the first content block for "
                        "high-signal opener patterns, not full rhetorical intent."
                    ),
                    rewrite_tactics=(
                        "Start the section with one prose sentence that states purpose before structured blocks or definitions.",
                    ),
                )
            )
        return violations


def _section_opening_issue(
    first_content,
    *,
    definition_pattern,
    blocked_opening_kinds: frozenset[BlockKind],
) -> str | None:
    if first_content.kind in blocked_opening_kinds:
        return "blocked_block_kind_opening"
    if first_content.kind != BlockKind.PARAGRAPH:
        return None
    if not first_content.sentences:
        return None
    opening_text = first_content.sentences[0].source_text.strip()
    if not opening_text:
        return None
    if definition_pattern.search(opening_text):
        return "definitional_opening"
    return None


def _parse_heading_levels(raw: object) -> tuple[int, ...] | None:
    if raw is None:
        return None
    values: tuple[object, ...]
    if isinstance(raw, int):
        values = (raw,)
    elif isinstance(raw, (list, tuple)):
        values = tuple(raw)
    else:
        raise ValueError("apply_heading_levels must be an integer or sequence of integers")
    levels: list[int] = []
    for value in values:
        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError("apply_heading_levels must be an integer or sequence of integers")
        if value < 1:
            raise ValueError("apply_heading_levels must contain levels >= 1")
        levels.append(value)
    return tuple(dict.fromkeys(levels))


def _resolve_heading_levels(raw: object) -> frozenset[int] | None:
    parsed = _parse_heading_levels(raw)
    if parsed is None:
        return None
    return frozenset(parsed)


def register(registry) -> None:
    registry.add(SectionOpenerBlockKindRule)
