"""Strict configuration parsing and validation.
"""

from __future__ import annotations

from typing import Any, Literal, Mapping

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StrictBool,
    ValidationError,
    field_validator,
)

from hermeneia.config.defaults import DEFAULT_PROFILE
from hermeneia.rules.base import Severity


class ConfigError(ValueError):
    """Raised when a configuration file is structurally invalid."""


class _ConfigModel(BaseModel):
    """Configmodel."""

    model_config = ConfigDict(extra="forbid", frozen=True)


class ProfileConfig(_ConfigModel):
    """Profileconfig."""

    model_config = ConfigDict(extra="forbid", frozen=True, populate_by_name=True)

    name: str = DEFAULT_PROFILE
    """Profile name."""
    audience: str | None = None
    """Configured audience profile."""
    genre: str | None = None
    """Configured writing genre."""
    section: str | None = None
    """Section-oriented profile policy."""
    register_name: str | None = Field(
        default=None, alias="register", serialization_alias="register"
    )
    """Optional register profile name."""

    @property
    def register(self) -> str | None:
        """Register.

        Returns
        -------
        str | None
            Resulting value produced by this call.
        """
        return self.register_name


class LanguageConfig(_ConfigModel):
    """Languageconfig."""

    code: str = "en"
    """Language code for the active language pack."""
    pack: str | None = None
    """Language pack implementation identifier."""


class EmbeddingConfig(_ConfigModel):
    """Embeddingconfig."""

    backend: Literal["none", "sentence_transformers"] = "none"
    """Embedding backend identifier."""
    model: str = "sentence-transformers/all-MiniLM-L6-v2"
    """Model name used by the backend."""


class RuntimeConfig(_ConfigModel):
    """Runtimeconfig."""

    strict_validation: StrictBool = True
    """Enable strict validation behavior."""
    experimental_rules: StrictBool = False
    """Enable experimental rules."""
    debug: StrictBool = False
    """Enable debug-mode diagnostics."""
    external_rule_modules: tuple[str, ...] = ()
    """External modules that contribute rules."""
    embeddings: EmbeddingConfig = Field(default_factory=EmbeddingConfig)
    """Enable embedding-backed features."""


class RuleOverrideConfig(_ConfigModel):
    """Ruleoverrideconfig."""

    enabled: StrictBool | None = None
    """Whether the feature is enabled."""
    severity: Severity | None = None
    """Severity assigned to the rule."""
    weight: float | None = None
    """Rule weight used by scoring."""
    options: dict[str, object] = Field(default_factory=dict)
    """Rule-specific option mapping."""
    extra_patterns: tuple[str, ...] = ()
    """Additional user-defined patterns."""
    silenced_patterns: tuple[str, ...] = ()
    """Patterns excluded from matching."""

    @field_validator("weight", mode="before")
    @classmethod
    def _validate_weight_type(cls, raw: object) -> object:
        """Validate weight type."""
        if raw is None:
            return None
        if isinstance(raw, bool) or not isinstance(raw, (int, float)):
            raise ValueError("rule override.weight must be numeric")
        return float(raw)


class RulesConfig(_ConfigModel):
    """Rulesconfig."""

    active: tuple[str, ...] | None = None
    """Explicitly activated rule identifiers."""
    disabled: tuple[str, ...] = ()
    """Explicitly disabled rule identifiers."""
    overrides: dict[str, RuleOverrideConfig] = Field(default_factory=dict)
    """Per-rule override configuration."""


class ScoringConfig(_ConfigModel):
    """Scoringconfig."""

    aggregation: str = "hierarchical"
    """Score aggregation strategy."""
    output: tuple[str, ...] = ("layer_scores", "global_score", "violation_list")
    """Output configuration block."""


class SuggestionConfig(_ConfigModel):
    """Suggestionconfig."""

    enabled: StrictBool = True
    """Whether the feature is enabled."""
    default_mode: str = "tactic_only"
    """Default suggestion mode."""


class ReportingConfig(_ConfigModel):
    """Reportingconfig."""

    format: str = "text"
    """Report output format."""
    sort_by: str = "severity_desc"
    """Diagnostic sorting strategy."""


class ProjectConfig(_ConfigModel):
    """Projectconfig."""

    profile: ProfileConfig = Field(default_factory=ProfileConfig)
    """Configured value for ``profile``."""
    language: LanguageConfig = Field(default_factory=LanguageConfig)
    """Language configuration block."""
    runtime: RuntimeConfig = Field(default_factory=RuntimeConfig)
    """Runtime configuration block."""
    rules: RulesConfig = Field(default_factory=RulesConfig)
    """Rule-selection configuration block."""
    scoring: ScoringConfig = Field(default_factory=ScoringConfig)
    """Scoring configuration block."""
    suggestions: SuggestionConfig = Field(default_factory=SuggestionConfig)
    """Suggestion configuration block."""
    reporting: ReportingConfig = Field(default_factory=ReportingConfig)
    """Reporting configuration block."""


def parse_project_config(raw: Mapping[str, object] | None) -> ProjectConfig:
    """Validate a raw mapping and return the typed config object.

    Parameters
    ----------
    raw : Mapping[str, object] | None
        Raw value before validation.

    Returns
    -------
    ProjectConfig
        Resulting value produced by this call.
    """

    if raw is None:
        return ProjectConfig()
    if not isinstance(raw, Mapping):
        raise ConfigError("root must be a mapping")
    try:
        return ProjectConfig.model_validate(raw)
    except ValidationError as exc:
        raise ConfigError(_format_validation_error(exc)) from exc


def _format_validation_error(exc: ValidationError) -> str:
    """Format validation error."""
    errors = exc.errors(include_url=False)
    return "; ".join(_format_single_validation_error(error) for error in errors)


def _format_single_validation_error(error: Mapping[str, Any]) -> str:
    """Format single validation error."""
    loc = tuple(str(entry) for entry in error.get("loc", ()))
    if error.get("type") == "extra_forbidden" and loc:
        scope = ".".join(loc[:-1]) or "root"
        return f"Unknown field '{loc[-1]}' in {scope}"
    scope = ".".join(loc) or "root"
    message = str(error.get("msg", "invalid value"))
    return f"{scope}: {message}"
