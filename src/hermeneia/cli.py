"""CLI adapter for the Hermeneia analysis pipeline."""

from __future__ import annotations

import dataclasses
import json
from pathlib import Path

import typer

from hermeneia import __version__, info
from hermeneia.config.loader import load_project_config
from hermeneia.config.profile import CliOverrides, ProfileResolver
from hermeneia.config.schema import ProjectConfig
from hermeneia.engine.registry import RuleRegistry
from hermeneia.engine.runner import AnalysisInput, AnalysisPolicy, AnalysisResult, AnalysisRunner
from hermeneia.infrastructure.embeddings import build_embedding_backend
from hermeneia.language.registry import LanguageRegistry
from hermeneia.document.annotator import SpaCyDocumentAnnotator
from hermeneia.document.markdown import MarkdownDocumentParser
from hermeneia.document.model import SourceKind
from hermeneia.document.structured import project, project_frontmatter, source_kind
from hermeneia.infrastructure.changes import changed_files, changed_lines
from hermeneia.infrastructure.lexicon_files import load_terms
from hermeneia.language.base import LanguagePack
from hermeneia.report.annotations import build_excerpt
from hermeneia.report.sarif import sarif_log
from hermeneia.rules.base import Severity, SuggestionMode, Violation
from hermeneia.rules.loader import load_builtin_rules, load_external_rules

app = typer.Typer(add_completion=False, no_args_is_help=True)

SUPPORTED_SCORING_OUTPUTS = frozenset({"layer_scores", "global_score", "violation_list"})
#: Names of the project configuration file, searched from the target upwards.
CONFIG_NAMES = (".hermeneia.yaml", ".hermeneia.yml")


@app.command("info")
def cli_info() -> None:
    """Display version and platform diagnostics."""

    typer.echo(info())


@app.command("lint")
def cli_lint(
    targets: list[Path] = typer.Argument(..., exists=True, readable=True, resolve_path=True),
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
        None, "--format", help="Output format: text, compact, json or sarif."
    ),
    output: Path | None = typer.Option(
        None, "--output", help="File receiving the SARIF log, instead of standard output."
    ),
    root: Path | None = typer.Option(
        None,
        "--root",
        help="Root against which the SARIF log states paths; default: current folder.",
    ),
    rule: list[str] = typer.Option([], "--rule", help="Restrict analysis to these rule ids."),
    disable_rule: list[str] = typer.Option(
        [], "--disable-rule", help="Disable specific rule ids after profile resolution."
    ),
    load_rules: list[str] = typer.Option(
        [], "--load-rules", help="External rule modules exposing register(registry)."
    ),
    experimental: bool = typer.Option(False, "--experimental", help="Enable experimental rules."),
    fail_on: Severity = typer.Option(
        Severity.ERROR,
        "--fail-on",
        help="Exit non-zero when this severity or higher is present.",
    ),
    changed: bool = typer.Option(
        False, "--changed", help="Report only the findings on lines changed since --base."
    ),
    base: str = typer.Option("HEAD", "--base", help="Revision compared by --changed."),
    kinds: list[str] = typer.Option(
        [],
        "--kind",
        help="Source kinds collected from a directory (markdown, yaml, python, commit).",
    ),
    no_exclude: bool = typer.Option(
        False, "--no-exclude", help="Collect the directories excluded by inputs.exclude_dirs."
    ),
) -> None:
    """Lint Markdown files, structured sources, or directories.

    Parameters
    ----------
    targets : list[Path]
        Files or directories to analyse; the configuration is searched from the first one.
    profile : str
        Resolved profile controlling rule behavior.
    config : Path | None
        Resolved configuration used by this operation.
    output_format : str | None
        Input value for ``output_format``.
    output : Path | None
        File receiving the SARIF log; standard output when absent.
    root : Path | None
        Root of the consumer repository, against which the SARIF log states every path.
    rule : list[str]
        Input value for ``rule``.
    disable_rule : list[str]
        Input value for ``disable_rule``.
    load_rules : list[str]
        Input value for ``load_rules``.
    experimental : bool
        Input value for ``experimental``.
    fail_on : Severity
        Input value for ``fail_on``.
    changed : bool
        Whether to report only the findings on lines changed since ``base``.
    base : str
        Revision compared by ``changed``.
    kinds : list[str]
        Source kinds collected from a directory, overriding ``inputs.kinds``.
    no_exclude : bool
        Whether to collect the directories excluded by ``inputs.exclude_dirs``.
    """

    try:
        config = config or _discover_config(targets[0])
        project_config = load_project_config(config)
        effective_format = output_format or project_config.reporting.format
        if effective_format == "sarif" and changed:
            raise typer.BadParameter(
                "the SARIF format reports every finding, so it cannot be combined with --changed."
            )
        if effective_format != "sarif" and (output is not None or root is not None):
            raise typer.BadParameter("--output and --root require the SARIF format.")
        registry = RuleRegistry()
        load_builtin_rules(registry)
        for module_name in (*project_config.runtime.external_rule_modules, *load_rules):
            load_external_rules(module_name, registry)

        language_registry = LanguageRegistry()
        language_pack = _with_terms(
            language_registry.get(project_config.language.code),
            load_terms(project_config.terminology, config.parent if config else Path.cwd()),
        )
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
        collected_kinds = frozenset(
            SourceKind(kind) for kind in (kinds or project_config.inputs.kinds)
        )
        excluded = () if no_exclude else project_config.inputs.exclude_dirs
        inputs = tuple(
            item
            for target in targets
            for item in _collect_inputs(
                target,
                collected_kinds,
                excluded,
                changed_files(target, base) if changed and target.is_dir() else None,
                frozenset(project_config.inputs.frontmatter_keys),
            )
        )
        if not inputs:
            if changed:
                return
            raise typer.BadParameter("No analysable files were found at the requested target.")
        batch = runner.analyze(inputs, resolved_profile)
        if changed:
            batch = _restrict_to_changes(batch, base)

        if effective_format == "sarif":
            log = sarif_log(batch, registry.all(), __version__, root or Path.cwd())
            _write_or_echo(json.dumps(log, indent=2, ensure_ascii=False), output)
        elif effective_format == "json":
            typer.echo(_render_json(batch))
        elif effective_format == "compact":
            typer.echo(_render_compact(batch))
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
    """Root command for the Hermeneia command-line interface.

    Parameters
    ----------
    version : bool
        Input value for ``version``.
    """

    if version:
        typer.echo(__version__)
        raise typer.Exit()


def _discover_config(target: Path) -> Path | None:
    """Return the nearest project configuration file at or above a target, if any."""
    directory = target if target.is_dir() else target.parent
    for candidate in (directory, *directory.parents):
        for name in CONFIG_NAMES:
            if (candidate / name).is_file():
                return candidate / name
    return None


def _with_terms(language_pack: LanguagePack, terms: frozenset[str]) -> LanguagePack:
    """Return a language pack reading the terms of a project as named quantities."""
    if not terms:
        return language_pack
    lexicons = dataclasses.replace(
        language_pack.lexicons,
        nominalization_allowlist=language_pack.lexicons.nominalization_allowlist | terms,
    )
    return dataclasses.replace(language_pack, lexicons=lexicons)


def _collect_inputs(
    target: Path,
    kinds: frozenset[SourceKind],
    exclude_dirs: tuple[str, ...],
    paths: tuple[Path, ...] | None = None,
    frontmatter_keys: frozenset[str] = frozenset(),
) -> tuple[AnalysisInput, ...]:
    """Collect the sources of a target, each projected to Markdown when it is structured.

    A file target is analysed whatever its kind. A directory target yields its files of the
    requested kinds, outside the excluded directories, or only the listed paths when given. A
    Markdown file also yields the values of its frontmatter keys listed in ``frontmatter_keys``,
    analysed as a structured source located in the same file.
    """
    if target.is_file():
        candidates: tuple[Path, ...] = (target,)
    else:
        pool = paths if paths is not None else tuple(sorted(target.rglob("*")))
        candidates = tuple(
            path
            for path in pool
            if path.is_file()
            and source_kind(path) in kinds
            and not any(part in exclude_dirs for part in path.relative_to(target).parts[:-1])
        )
    inputs: list[AnalysisInput] = []
    for path in candidates:
        kind = source_kind(path) or SourceKind.MARKDOWN
        text = path.read_text(encoding="utf-8")
        projections = [(kind, project(kind, text))]
        if kind == SourceKind.MARKDOWN and frontmatter_keys:
            frontmatter = project_frontmatter(text, frontmatter_keys)
            if frontmatter.fields:
                projections.append((SourceKind.YAML, frontmatter))
        inputs.extend(
            AnalysisInput(
                path=path,
                source=projection.markdown,
                source_kind=projected_kind,
                fields=projection.fields,
                line_map=projection.line_map,
            )
            for projected_kind, projection in projections
        )
    return tuple(inputs)


def _restrict_to_changes(batch, base: str):
    """Keep the findings whose source lines intersect the lines changed since a base revision."""
    results = []
    for result in batch.results:
        path = result.report.path
        lines = changed_lines(path, base) if path is not None else None
        if lines is None:
            results.append(result)
            continue
        document = result.document
        kept = tuple(
            violation
            for violation in result.violations
            if any(
                document.source_line(line) in lines
                for line in range(violation.span.start_line, violation.span.end_line + 1)
            )
        )
        report = dataclasses.replace(result.report, violations=kept)
        results.append(dataclasses.replace(result, violations=kept, report=report))
    return dataclasses.replace(batch, results=tuple(results))


def _render_compact(batch) -> str:
    """Render one line per finding, located in the source file."""
    lines: list[str] = []
    for diagnostic in batch.diagnostics:
        location = f"{diagnostic.path}: " if diagnostic.path is not None else ""
        lines.append(f"[diagnostic] {location}{diagnostic.message}")
    for result in batch.results:
        path_label = str(result.report.path) if result.report.path is not None else "<memory>"
        for violation in result.violations:
            document = result.document
            location = f"{document.source_line(violation.span.start_line)}"
            if document.source_kind == SourceKind.MARKDOWN:
                location += f":{violation.span.start_column}"
            lines.append(
                f"{path_label}:{location}: "
                f"{violation.severity.value} {violation.rule_id}: {violation.message}"
            )
    return "\n".join(lines)


def _render_text(batch) -> str:
    """Render text."""
    lines: list[str] = []
    for diagnostic in batch.diagnostics:
        location = f"{diagnostic.path}: " if diagnostic.path is not None else ""
        lines.append(f"[diagnostic] {location}{diagnostic.message}")
    for result in batch.results:
        path_label = str(result.report.path) if result.report.path is not None else "<memory>"
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
                lines.append(f"    {result.document.source_line(row.line_number)}: {row.line_text}")
                lines.append(f"       {row.marker_line}")
            _append_violation_details(lines, violation)
        if result.report.scorecard is not None and "global_score" in result.report.scoring_output:
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
        "results": [_located(result) for result in batch.results],
    }
    return json.dumps(payload, indent=2, sort_keys=True)


def _located(result: AnalysisResult) -> dict[str, object]:
    """Return the report of a result, with every span located in the source file."""
    payload: dict[str, object] = result.report.to_dict()
    violations = payload.get("violations", [])
    for violation in violations if isinstance(violations, list) else []:
        span = violation.get("span")
        if isinstance(span, dict):
            for key in ("start_line", "end_line"):
                span[key] = result.document.source_line(span[key])
    return payload


def _write_or_echo(text: str, output: Path | None) -> None:
    """Write ``text`` to ``output``, creating its folder, or echo it when ``output`` is absent."""
    if output is None:
        typer.echo(text)
        return
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text + "\n", encoding="utf-8")


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
            "Unsupported scoring.aggregation " f"'{scoring_aggregation}'. Expected 'hierarchical'."
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
