# Copilot Instructions for petstore-test-python

## Project Overview

This is a **Python test repository** for the Swagger Petstore API and UI.
It uses `pytest` (never `unittest`) with the following layers:

- `framework/` – shared test framework (API client, UI client, assertions, POM)
- `tests/api/` – REST API tests using `requests`
- `tests/ui/` – Selenium browser tests with Page Object Model
- `tests/integration/` – multi-component integration tests
- `tests/e2e/` – full user-journey end-to-end tests
- `tests/performance/` – benchmark tests (manual only, never in CI)

## Key Conventions

### Test Style
- Always use `pytest`, never `unittest`.
- Use **fluent assertions** from `framework.assertions`: `assert_that(x).equals(y)`.
- For HTTP responses use `assert_response(resp).is_ok().json_has_key("id")`.
- Mark tests with the appropriate marker: `@pytest.mark.api`, `@pytest.mark.ui`, etc.
- Use **factory_boy** factories from `framework.factories` to generate test data.

### Shared Interface
- Both `PetstoreApiClient` and `PetstoreUiClient` implement `PetstoreClientProtocol`.
- Tests that can run against both should be parameterised over the protocol.

### Page Object Model (POM)
- All page interactions live in `framework/pages/`.
- Page objects extend `BasePage` and return `self` for method chaining.
- Locators are class-level tuples `(By.ID, "selector")`.

### File Organisation
- One test class per feature/endpoint.
- Fixtures live in `conftest.py` at the appropriate scope level.
- Global fixtures (api_client, browser, ui_client) are in `tests/conftest.py`.
- Suite-specific fixtures (new_pet, etc.) are in `tests/<suite>/conftest.py`.

## Package Manager

Use **uv** for all dependency management:
```bash
uv sync           # install deps
uv run pytest     # run tests
uv run mypy framework/
uv run ruff check .
uv run black .
```

Never use `pip install` directly in this project.

## Code Quality

- All code must pass `ruff`, `black`, and `mypy` before merging.
- Run `uv run pre-commit run --all-files` before opening a PR.
- Type annotations are **required** on all framework code.
- Test files may omit return type annotations for brevity.

## CI/CD

- API, integration, and E2E tests run automatically on every PR.
- UI tests run in CI with `RUN_UI_TESTS=1` and headless Chrome.
- Performance tests **never** run in CI – they are manual only.
- Coverage is published to Codecov; Allure reports to GitHub Pages.

## Secrets

- In CI: use GitHub Secrets (`CODECOV_TOKEN`, etc.).
- Locally: use 1Password CLI: `op run --env-file=.env.local -- uv run pytest`.
- **Never** commit secrets to the repository.

## Adding New Tests

1. Create the test file in the appropriate `tests/<suite>/` directory.
2. Add the correct marker (`@pytest.mark.api`, etc.).
3. Use `assert_that()` / `assert_response()` for all assertions.
4. Use factories for test data; avoid hard-coded IDs.
5. Clean up any created resources in `finally` blocks or dedicated teardown fixtures.
6. Run `uv run pytest tests/<suite>/ -v` to verify locally.
