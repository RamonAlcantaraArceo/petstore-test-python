# petstore-test-python

A structured Python test repository supporting **API**, **UI** (Selenium + POM), **integration**, and **end-to-end** testing of the [Swagger Petstore](https://petstore-api-dev.ramon-alcantara.work/docs) with a shared interface and fluent assertions.

## Features

- ✅ **pytest** (not unittest) with marks for every test category
- ✅ **Shared interface** – write a test once, run it against API *or* UI
- ✅ **Fluent assertions** (`assert_that(value).equals(expected)`)
- ✅ **Selenium + Page Object Model** for UI tests
- ✅ **requests** library for API tests
- ✅ **Allure Report 3** test reporting
- ✅ **Codecov** coverage publishing
- ✅ **GitHub Actions** CI/CD pipeline
- ✅ **MkDocs + Material** documentation
- ✅ **factory_boy + Faker** test data generation
- ✅ **mypy**, **ruff**, **black**, **pre-commit** code quality gates

## Quick Start

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Installation

```bash
git clone https://github.com/RamonAlcantaraArceo/petstore-test-python.git
cd petstore-test-python
uv venv --seed
uv sync --all-extras --all-groups
```

### Running Tests

```bash
# All API tests
uv run pytest tests/api/ -m api -v

# All integration tests
uv run pytest tests/integration/ -m integration -v

# All E2E tests
uv run pytest tests/e2e/ -m e2e -v

# UI tests (requires Chrome; disabled by default)
RUN_UI_TESTS=1 uv run pytest tests/ui/ -m ui -v

# All non-UI, non-performance tests
uv run pytest -m "not ui and not performance" -v

# With coverage
uv run pytest tests/api/ --cov=framework --cov-report=term-missing

# Performance benchmarks (manual only)
uv run pytest tests/performance/ --benchmark-only
```

### With Allure Reports

```bash
# 1. Run tests and collect Allure results
uv run pytest tests/api/ --alluredir=allure-results

# 2. Generate the HTML report using Allure 3 CLI (requires Node.js)
npx allure generate -o allure-report

# 3. Open the report in a browser
npx allure open allure-report
```

> **Note:** Install Allure CLI globally for convenience: `npm install -g allure`

## Directory Structure

```
petstore-test-python/
├── .github/
│   ├── workflows/
│   │   ├── ci.yml          # Main CI pipeline
│   │   └── docs.yml        # Documentation deployment
│   └── copilot-instructions.md
├── docs/                   # MkDocs documentation source
├── framework/              # Shared test framework
│   ├── api_client.py       # REST API client (requests)
│   ├── ui_client.py        # Browser client (Selenium)
│   ├── assertions.py       # Fluent assertion helpers
│   ├── interfaces.py       # Common PetstoreClientProtocol
│   ├── factories.py        # Test-data factories
│   └── pages/              # Page Object Model
│       ├── base_page.py
│       ├── login_page.py
│       └── pets_page.py
├── tests/
│   ├── conftest.py         # Global fixtures
│   ├── api/                # API tests
│   ├── ui/                 # UI / Selenium tests
│   ├── integration/        # Integration tests
│   ├── e2e/                # End-to-end tests
│   └── performance/        # Benchmark tests (manual)
├── pyproject.toml          # Project config (uv + pytest + tools)
├── mkdocs.yml              # Documentation config
└── .pre-commit-config.yaml
```

## Shared Interface Pattern

The key design principle is that API and UI clients implement the same
`PetstoreClientProtocol`.  Tests can be parameterised to run against both:

```python
@pytest.mark.parametrize("client_fixture", ["api_client", "ui_client"], indirect=True)
def test_login(client):
    client.login("user1", "password1")
    assert_that(client.is_logged_in()).is_true()
```

## Fluent Assertions

```python
from framework.assertions import assert_that, assert_response

assert_that(pet["name"]).equals("Fido")
assert_that(pets).is_not_empty().has_length_greater_than(0)
assert_that(token).contains("logged in user session")

assert_response(response).is_ok().json_has_key("id")
```

## Environment Variables

| Variable                | Default                              | Description                        |
|-------------------------|--------------------------------------|------------------------------------|
| `PETSTORE_API_BASE_URL` | `http://localhost:8000`              | Petstore API root                  |
| `PETSTORE_UI_BASE_URL`  | `https://the-internet.herokuapp.com` | Web UI root                        |
| `RUN_UI_TESTS`          | `0`                                  | Set to `1` to enable UI tests      |
| `HEADLESS`              | `true`                               | Set to `false` for visible browser |

## Local Secrets with 1Password CLI

```bash
op run --env-file=.env.local -- uv run pytest tests/api/ -v
```

Create `.env.local` (gitignored):

```bash
PETSTORE_API_KEY=op://vault/petstore/api_key
CODECOV_TOKEN=op://vault/codecov/token
```

## Pre-commit Hooks

```bash
uv run pre-commit install
uv run pre-commit run --all-files
```
