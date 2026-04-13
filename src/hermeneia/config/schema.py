"""Strict configuration parsing and validation.

Classes
-------
ConfigError
    Public API symbol.
ProfileConfig
    Public API symbol.
LanguageConfig
    Public API symbol.
EmbeddingConfig
    Public API symbol.
RuntimeConfig
    Public API symbol.
RuleOverrideConfig
    Public API symbol.
RulesConfig
    Public API symbol.
ScoringConfig
    Public API symbol.
SuggestionConfig
    Public API symbol.
ReportingConfig
    Public API symbol.
ProjectConfig
    Public API symbol.

Functions
---------
parse_project_config
    Public API symbol.
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
    """Profileconfig.

    Attributes
    ----------
    audience : str | None
        Configured audience profile.
    genre : str | None
        Configured writing genre.
    name : str
        Profile name.
    register_name : str | None
        Optional register profile name.
    section : str | None
        Section-oriented profile policy.
    """

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
        """Register.

        Returns
        -------
        str | None
            Resulting value produced by this call.
        """
        return self.register_name


class LanguageConfig(_ConfigModel):
    """Languageconfig.

    Attributes
    ----------
    code : str
        Language code for the active language pack.
    pack : str | None
        Language pack implementation identifier.
    """

    code: str = "en"
    pack: str | None = None


class EmbeddingConfig(_ConfigModel):
    """Embeddingconfig.

    Attributes
    ----------
    backend : Literal['none', 'sentence_transformers']
        Embedding backend identifier.
    model : str
        Model name used by the backend.
    """

    backend: Literal["none", "sentence_transformers"] = "none"
    model: str = "sentence-transformers/all-MiniLM-L6-v2"


class RuntimeConfig(_ConfigModel):
    """Runtimeconfig.

    Attributes
    ----------
    debug : StrictBool
        Enable debug-mode diagnostics.
    embeddings : EmbeddingConfig
        Enable embedding-backed features.
    experimental_rules : StrictBool
        Enable experimental rules.
    external_rule_modules : tuple[str, ...]
        External modules that contribute rules.
    strict_validation : StrictBool
        Enable strict validation behavior.
    """

    strict_validation: StrictBool = True
    experimental_rules: StrictBool = False
    debug: StrictBool = False
    external_rule_modules: tuple[str, ...] = ()
    embeddings: EmbeddingConfig = Field(default_factory=EmbeddingConfig)


class RuleOverrideConfig(_ConfigModel):
    """Ruleoverrideconfig.

    Attributes
    ----------
    enabled : StrictBool | None
        Whether the feature is enabled.
    extra_patterns : tuple[str, ...]
        Additional user-defined patterns.
    options : dict[str, object]
        Rule-specific option mapping.
    severity : Severity | None
        Severity assigned to the rule.
    silenced_patterns : tuple[str, ...]
        Patterns excluded from matching.
    weight : float | None
        Rule weight used by scoring.
    """

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
    """Rulesconfig.

    Attributes
    ----------
    active : tuple[str, ...] | None
        Explicitly activated rule identifiers.
    disabled : tuple[str, ...]
        Explicitly disabled rule identifiers.
    overrides : dict[str, RuleOverrideConfig]
        Per-rule override configuration.
    """

    active: tuple[str, ...] | None = None
    disabled: tuple[str, ...] = ()
    overrides: dict[str, RuleOverrideConfig] = Field(default_factory=dict)


class ScoringConfig(_ConfigModel):
    """Scoringconfig.

    Attributes
    ----------
    aggregation : str
        Score aggregation strategy.
    output : tuple[str, ...]
        Output configuration block.
    """

    aggregation: str = "hierarchical"
    output: tuple[str, ...] = ("layer_scores", "global_score", "violation_list")


class SuggestionConfig(_ConfigModel):
    """Suggestionconfig.

    Attributes
    ----------
    default_mode : str
        Default suggestion mode.
    enabled : StrictBool
        Whether the feature is enabled.
    """

    enabled: StrictBool = True
    default_mode: str = "tactic_only"


class ReportingConfig(_ConfigModel):
    """Reportingconfig.

    Attributes
    ----------
    format : str
        Report output format.
    sort_by : str
        Diagnostic sorting strategy.
    """

    format: str = "text"
    sort_by: str = "severity_desc"


class ProjectConfig(_ConfigModel):
    """Projectconfig.

    Attributes
    ----------
    language : LanguageConfig
        Language configuration block.
    profile : ProfileConfig
        Configured value for ``profile``.
    reporting : ReportingConfig
        Reporting configuration block.
    rules : RulesConfig
        Rule-selection configuration block.
    runtime : RuntimeConfig
        Runtime configuration block.
    scoring : ScoringConfig
        Scoring configuration block.
    suggestions : SuggestionConfig
        Suggestion configuration block.
    """

    profile: ProfileConfig = Field(default_factory=ProfileConfig)
    language: LanguageConfig = Field(default_factory=LanguageConfig)
    runtime: RuntimeConfig = Field(default_factory=RuntimeConfig)
    rules: RulesConfig = Field(default_factory=RulesConfig)
    scoring: ScoringConfig = Field(default_factory=ScoringConfig)
    suggestions: SuggestionConfig = Field(default_factory=SuggestionConfig)
    reporting: ReportingConfig = Field(default_factory=ReportingConfig)


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
