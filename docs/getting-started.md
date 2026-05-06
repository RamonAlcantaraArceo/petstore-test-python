# Getting Started

## Prerequisites

- Python 3.12 or later
- [uv](https://docs.astral.sh/uv/) – fast Python package manager

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Clone & Install

```bash
git clone https://github.com/RamonAlcantaraArceo/petstore-test-python.git
cd petstore-test-python
uv sync
```

`uv sync` installs all development dependencies defined in `pyproject.toml`.

## Running Tests

```bash
# API tests only
uv run pytest tests/api/ -m api -v

# Integration tests
uv run pytest tests/integration/ -m integration -v

# E2E tests
uv run pytest tests/e2e/ -m e2e -v

# All non-UI, non-benchmark tests
uv run pytest -m "not ui and not performance" -v

# With HTML coverage report
uv run pytest tests/api/ --cov=framework --cov-report=html
```

## Pre-commit Hooks

Install the hooks once after cloning:

```bash
uv run pre-commit install
```

Run against all files manually:

```bash
uv run pre-commit run --all-files
```

## Environment Configuration

| Variable | Default | Description |
|---|---|---|
| `PETSTORE_API_BASE_URL` | `http://localhost:8000` | API root URL |
| `PETSTORE_UI_BASE_URL` | `https://the-internet.herokuapp.com` | UI root URL |
| `RUN_UI_TESTS` | `0` | Set to `1` to enable Selenium tests |
| `HEADLESS` | `true` | Browser headless mode |

## Local Secrets (1Password CLI)

```bash
op run --env-file=.env.local -- uv run pytest tests/api/ -v
```

`.env.local` example (never commit this file):

```ini
PETSTORE_API_KEY=op://MyVault/petstore/api_key
CODECOV_TOKEN=op://MyVault/codecov/token
```
