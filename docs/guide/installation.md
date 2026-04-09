# Installation

This guide indicates how to set up a reproducible environment where `hermeneia` can run deterministically.

## Prerequisites

- Python `3.12`
- `conda` (recommended for this repository)

## Recommended Setup (From Source)

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

Install optional embedding dependencies (used by optional embedding-backed heuristics):

```sh
pip install -e ".[semantic]"
```

## Notes

- The environment pins spaCy model compatibility for deterministic test behavior.
- Without editable installation, commands can still run by setting `PYTHONPATH=src`.

After installation, go to [Usage](usage.md) for command workflow and to [Configuration](configuration.md) for policy tuning.
