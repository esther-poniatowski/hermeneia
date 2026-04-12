"""CLI adapter for the Hermeneia analysis pipeline."""

from __future__ import annotations

import json
from pathlib import Path

import typer

from hermeneia import __version__, info
from hermeneia.config.loader import load_project_config
from hermeneia.config.profile import CliOverrides, ProfileResolver
from hermeneia.config.schema import ProjectConfig
from hermeneia.engine.registry import RuleRegistry
from hermeneia.engine.runner import AnalysisInput, AnalysisPolicy, AnalysisRunner
from hermeneia.infrastructure.embeddings import build_embedding_backend
from hermeneia.language.registry import LanguageRegistry
from hermeneia.document.annotator import SpaCyDocumentAnnotator
from hermeneia.document.markdown import MarkdownDocumentParser
from hermeneia.report.annotations import build_excerpt
from hermeneia.rules.base import Severity, SuggestionMode, Violation
from hermeneia.rules.loader import load_builtin_rules, load_external_rules

app = typer.Typer(add_completion=False, no_args_is_help=True)

SUPPORTED_SCORING_OUTPUTS = frozenset(
    {"layer_scores", "global_score", "violation_list"}
)


@app.command("info")
def cli_info() -> None:
    """Display version and platform diagnostics."""

    typer.echo(info())


@app.command("lint")
def cli_lint(
    target: Path = typer.Argument(..., exists=True, readable=True, resolve_path=True),
    profile: str = typer.Option(
        "research", "--profile", help="Profile preset to resolve before user overrides."
    ),
    config: Path | None = typer.Option(
        None,
        "--config",
        exists=True,
        readable=True,
        resolve_path=True,
        help="Project YAML configuration.",
    ),
    output_format: str | None = typer.Option(
        None, "--format", help="Output format: text or json."
    ),
    rule: list[str] = typer.Option(
        [], "--rule", help="Restrict analysis to these rule ids."
    ),
    disable_rule: list[str] = typer.Option(
        [], "--disable-rule", help="Disable specific rule ids after profile resolution."
    ),
    load_rules: list[str] = typer.Option(
        [], "--load-rules", help="External rule modules exposing register(registry)."
    ),
    experimental: bool = typer.Option(
        False, "--experimental", help="Enable experimental rules."
    ),
    fail_on: Severity = typer.Option(
        Severity.ERROR,
        "--fail-on",
        help="Exit non-zero when this severity or higher is present.",
    ),
) -> None:
    """Lint a markdown file or directory."""

    try:
        project_config = load_project_config(config)
        registry = RuleRegistry()
        load_builtin_rules(registry)
        for module_name in (*project_config.runtime.external_rule_modules, *load_rules):
            load_external_rules(module_name, registry)

        language_registry = LanguageRegistry()
        language_pack = language_registry.get(project_config.language.code)
        resolved_profile = ProfileResolver(registry).resolve(
            project_config,
            language_pack,
            cli=CliOverrides(
                profile_name=profile,
                rule_ids=tuple(rule),
                disabled_rule_ids=tuple(disable_rule),
                reporting_format=output_format,
                enable_experimental=experimental,
            ),
        )
        embedding_backend = build_embedding_backend(project_config.runtime.embeddings)
        policy = _analysis_policy_from_config(project_config)

        runner = AnalysisRunner(
            parser=MarkdownDocumentParser(language_pack),
            annotator=SpaCyDocumentAnnotator(language_pack.parser_model),
            registry=registry,
            language_pack=language_pack,
            embedding_backend=embedding_backend,
            policy=policy,
        )
        inputs = _collect_inputs(target)
        if not inputs:
            raise typer.BadParameter(
                "No markdown files were found at the requested target."
            )
        batch = runner.analyze(inputs, resolved_profile)

        effective_format = output_format or project_config.reporting.format
        if effective_format == "json":
            typer.echo(_render_json(batch))
        else:
            typer.echo(_render_text(batch))

        if _has_failure(batch, fail_on):
            raise typer.Exit(code=1)
    except typer.Exit:
        raise
    except Exception as exc:  # pragma: no cover - CLI boundary guard
        typer.echo(f"error: {exc}", err=True)
        raise typer.Exit(code=2) from exc


@app.callback()
def main_callback(
    version: bool = typer.Option(
        False, "--version", "-v", help="Show the package version and exit."
    )
) -> None:
    """Root command for the Hermeneia command-line interface."""

    if version:
        typer.echo(__version__)
        raise typer.Exit()


def _collect_inputs(target: Path) -> tuple[AnalysisInput, ...]:
    """Collect inputs."""
    if target.is_file():
        return (AnalysisInput(path=target, source=target.read_text(encoding="utf-8")),)
    files = sorted(
        path
        for path in target.rglob("*")
        if path.is_file() and path.suffix.lower() in {".md", ".markdown"}
    )
    return tuple(
        AnalysisInput(path=path, source=path.read_text(encoding="utf-8"))
        for path in files
    )


def _render_text(batch) -> str:
    """Render text."""
    lines: list[str] = []
    for diagnostic in batch.diagnostics:
        location = f"{diagnostic.path}: " if diagnostic.path is not None else ""
        lines.append(f"[diagnostic] {location}{diagnostic.message}")
    for result in batch.results:
        path_label = (
            str(result.report.path) if result.report.path is not None else "<memory>"
        )
        lines.append(f"{path_label}:")
        if not result.violations:
            lines.append("  no violations")
            continue
        for violation in result.violations:
            excerpt = build_excerpt(result.document.source, violation.span)
            lines.append(
                f"  {violation.severity.value.upper()} {violation.rule_id}: {violation.message}"
            )
            for row in excerpt.lines:
                lines.append(f"    {row.line_number}: {row.line_text}")
                lines.append(f"       {row.marker_line}")
            _append_violation_details(lines, violation)
        if (
            result.report.scorecard is not None
            and "global_score" in result.report.scoring_output
        ):
            lines.append(f"  global score: {result.report.scorecard.global_score}")
    return "\n".join(lines)


def _render_json(batch) -> str:
    """Render json."""
    payload = {
        "diagnostics": [
            {
                "code": diagnostic.code,
                "message": diagnostic.message,
                "path": str(diagnostic.path) if diagnostic.path else None,
            }
            for diagnostic in batch.diagnostics
        ],
        "results": [result.report.to_dict() for result in batch.results],
    }
    return json.dumps(payload, indent=2, sort_keys=True)


def _has_failure(batch, threshold: Severity) -> bool:
    """Has failure."""
    ranks = {Severity.INFO: 1, Severity.WARNING: 2, Severity.ERROR: 3}
    minimum = ranks[threshold]
    return any(
        ranks[violation.severity] >= minimum
        for result in batch.results
        for violation in result.violations
    )


def _append_violation_details(lines: list[str], violation: Violation) -> None:
    """Append violation details."""
    evidence = violation.evidence
    if evidence is not None:
        if evidence.score is not None:
            lines.append(f"    evidence.score={evidence.score:.3f}")
        if evidence.threshold is not None:
            lines.append(f"    evidence.threshold={evidence.threshold:.3f}")
        if evidence.features:
            lines.append(
                "    evidence.features="
                + json.dumps(evidence.features, sort_keys=True, ensure_ascii=False)
            )
        if evidence.upstream_limits:
            lines.append(
                "    evidence.upstream_limits="
                + json.dumps(evidence.upstream_limits, ensure_ascii=False)
            )
    if violation.confidence is not None:
        lines.append(f"    confidence={violation.confidence:.3f}")
    if violation.rationale:
        lines.append(f"    rationale={violation.rationale}")


def _analysis_policy_from_config(project_config: ProjectConfig) -> AnalysisPolicy:
    """Analysis policy from config."""
    scoring_aggregation = project_config.scoring.aggregation
    if scoring_aggregation != "hierarchical":
        raise ValueError(
            "Unsupported scoring.aggregation "
            f"'{scoring_aggregation}'. Expected 'hierarchical'."
        )
    scoring_output = frozenset(project_config.scoring.output)
    unknown_outputs = sorted(scoring_output - SUPPORTED_SCORING_OUTPUTS)
    if unknown_outputs:
        raise ValueError(
            "Unsupported scoring.output entries: "
            + ", ".join(unknown_outputs)
            + ". Supported values are: "
            + ", ".join(sorted(SUPPORTED_SCORING_OUTPUTS))
            + "."
        )
    try:
        suggestion_mode = SuggestionMode(project_config.suggestions.default_mode)
    except ValueError as exc:
        raise ValueError(
            "Unsupported suggestions.default_mode "
            f"'{project_config.suggestions.default_mode}'. "
            "Expected one of: template, tactic_only, none."
        ) from exc
    return AnalysisPolicy(
        scoring_aggregation=scoring_aggregation,
        scoring_output=scoring_output,
        debug_mode=project_config.runtime.debug,
        suggestions_enabled=project_config.suggestions.enabled,
        suggestion_default_mode=suggestion_mode,
    )
