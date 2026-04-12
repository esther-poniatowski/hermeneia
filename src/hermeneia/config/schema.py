"""Strict configuration parsing and validation."""

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
    audience: str | None = None
    genre: str | None = None
    section: str | None = None
    register_name: str | None = Field(
        default=None, alias="register", serialization_alias="register"
    )

    @property
    def register(self) -> str | None:
        """Register."""
        return self.register_name


class LanguageConfig(_ConfigModel):
    """Languageconfig."""

    code: str = "en"
    pack: str | None = None


class EmbeddingConfig(_ConfigModel):
    """Embeddingconfig."""

    backend: Literal["none", "sentence_transformers"] = "none"
    model: str = "sentence-transformers/all-MiniLM-L6-v2"


class RuntimeConfig(_ConfigModel):
    """Runtimeconfig."""

    strict_validation: StrictBool = True
    experimental_rules: StrictBool = False
    debug: StrictBool = False
    external_rule_modules: tuple[str, ...] = ()
    embeddings: EmbeddingConfig = Field(default_factory=EmbeddingConfig)


class RuleOverrideConfig(_ConfigModel):
    """Ruleoverrideconfig."""

    enabled: StrictBool | None = None
    severity: Severity | None = None
    weight: float | None = None
    options: dict[str, object] = Field(default_factory=dict)
    extra_patterns: tuple[str, ...] = ()
    silenced_patterns: tuple[str, ...] = ()

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
    disabled: tuple[str, ...] = ()
    overrides: dict[str, RuleOverrideConfig] = Field(default_factory=dict)


class ScoringConfig(_ConfigModel):
    """Scoringconfig."""

    aggregation: str = "hierarchical"
    output: tuple[str, ...] = ("layer_scores", "global_score", "violation_list")


class SuggestionConfig(_ConfigModel):
    """Suggestionconfig."""

    enabled: StrictBool = True
    default_mode: str = "tactic_only"


class ReportingConfig(_ConfigModel):
    """Reportingconfig."""

    format: str = "text"
    sort_by: str = "severity_desc"


class ProjectConfig(_ConfigModel):
    """Projectconfig."""

    profile: ProfileConfig = Field(default_factory=ProfileConfig)
    language: LanguageConfig = Field(default_factory=LanguageConfig)
    runtime: RuntimeConfig = Field(default_factory=RuntimeConfig)
    rules: RulesConfig = Field(default_factory=RulesConfig)
    scoring: ScoringConfig = Field(default_factory=ScoringConfig)
    suggestions: SuggestionConfig = Field(default_factory=SuggestionConfig)
    reporting: ReportingConfig = Field(default_factory=ReportingConfig)


def parse_project_config(raw: Mapping[str, object] | None) -> ProjectConfig:
    """Validate a raw mapping and return the typed config object."""

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
