# Installation

This page sets up a reproducible environment where `hermeneia` runs deterministically.
It focuses on environment and package setup only; command workflow starts in [Usage](usage.md).

## Prerequisites

- Python `3.12`
- `conda` (recommended for this repository)

## Recommended Setup (From Source)

Run these steps in order:

1. Clone the repository.

   ```sh
   git clone https://github.com/esther-poniatowski/hermeneia.git
   cd hermeneia
   ```

2. Create and activate the project environment.

   ```sh
   conda env create -f environment.yml
   conda activate hermeneia
   ```

3. Install hermeneia in editable mode.

   ```sh
   pip install -e .
   ```

4. Verify the CLI is available.

   ```sh
   hermeneia info
   ```

## Optional: Semantic Extras

Install optional embedding dependencies when embedding-backed heuristics are required:

```sh
pip install -e ".[semantic]"
```

## Notes

- The environment pins spaCy model compatibility for deterministic test behavior.
- Without editable installation, commands can still run by setting `PYTHONPATH=src`.

After setup, continue with [Usage](usage.md).
Then use [Configuration](configuration.md) to tune policy defaults and overrides.
