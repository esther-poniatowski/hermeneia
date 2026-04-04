# Configuration

Hermeneia has **no project-specific configuration** yet. No YAML config file,
no environment variables, and no runtime settings are read by the current
release.

## Third-Party Tool Configs

The `config/` directory contains configuration files for third-party
development tools used during hermeneia's own development. These files do not
affect hermeneia's behavior at runtime.

### `config/tools/`

| File | Tool |
| ---- | ---- |
| `black.toml` | Black (code formatter) |
| `mypy.ini` | Mypy (static type checker) |
| `pylintrc.ini` | Pylint (linter, main source) |
| `pylintrc_tests.ini` | Pylint (linter, test source) |
| `pyrightconfig.json` | Pyright (type checker) |
| `releaserc.toml` | semantic-release (versioning) |

### `config/dictionaries/`

| File | Contents |
| ---- | -------- |
| `project.txt` | Project-specific spelling allowlist |
| `python.txt` | Python ecosystem terms |
| `tools.txt` | Tool and library names |

These dictionaries feed spell-checking tools (e.g. codespell, cspell) during
CI, not hermeneia itself.

## Planned

Once the analysis engine exists, hermeneia will support project-level
configuration for profiles, rule selection, and severity overrides. The exact
format has not been decided.
