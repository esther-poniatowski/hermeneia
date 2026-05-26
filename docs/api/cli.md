<a id="command-line-interface"></a>

# Command-line interface

Typer adapter exposing the Hermeneia analysis pipeline as a CLI.

<a id="module-hermeneia.cli"></a>

<a id="cli-commands"></a>

## CLI commands

CLI adapter for the Hermeneia analysis pipeline.

<a id="hermeneia.cli.cli_info"></a>

### hermeneia.cli.cli_info()

Display version and platform diagnostics.

<a id="hermeneia.cli.cli_lint"></a>

### hermeneia.cli.cli_lint(target=<typer.models.ArgumentInfo object>, profile=<typer.models.OptionInfo object>, config=<typer.models.OptionInfo object>, output_format=<typer.models.OptionInfo object>, rule=<typer.models.OptionInfo object>, disable_rule=<typer.models.OptionInfo object>, load_rules=<typer.models.OptionInfo object>, experimental=<typer.models.OptionInfo object>, fail_on=<typer.models.OptionInfo object>)

Lint a markdown file or directory.

* **Parameters:**
  * **target** (*Path*) – Input value for `target`.
  * **profile** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Resolved profile controlling rule behavior.
  * **config** (*Path* *|* *None*) – Resolved configuration used by this operation.
  * **output_format** ([*str*](https://docs.python.org/3/library/stdtypes.html#str) *|* *None*) – Input value for `output_format`.
  * **rule** ([*list*](https://docs.python.org/3/library/stdtypes.html#list) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *]*) – Input value for `rule`.
  * **disable_rule** ([*list*](https://docs.python.org/3/library/stdtypes.html#list) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *]*) – Input value for `disable_rule`.
  * **load_rules** ([*list*](https://docs.python.org/3/library/stdtypes.html#list) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *]*) – Input value for `load_rules`.
  * **experimental** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) – Input value for `experimental`.
  * **fail_on** ([*Severity*](rules-base.md#hermeneia.rules.base.Severity)) – Input value for `fail_on`.

<a id="hermeneia.cli.main_callback"></a>

### hermeneia.cli.main_callback(version=<typer.models.OptionInfo object>)

Root command for the Hermeneia command-line interface.

* **Parameters:**
  **version** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) – Input value for `version`.
