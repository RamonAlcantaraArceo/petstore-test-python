# CI/CD

The repository uses **GitHub Actions** for automated testing and deployment.

## Workflows

### `ci.yml` – Main CI Pipeline

Triggered on every push and pull request to `main`.

| Job | Description |
|---|---|
| `lint` | ruff, black (format check), mypy |
| `api-tests` | Runs `tests/api/` with coverage |
| `integration-tests` | Runs `tests/integration/` with coverage |
| `e2e-tests` | Runs `tests/e2e/` with coverage |
| `ui-tests` | Runs `tests/ui/` with headless Chrome |
| `allure-report` | Merges results and publishes to GitHub Pages |

### `docs.yml` – Documentation Deployment

Triggered on pushes to `main` that touch `docs/` or `mkdocs.yml`.
Builds MkDocs and deploys to the `gh-pages` branch.

## Secrets

Configure these in **Settings → Secrets and variables → Actions**:

| Secret | Description |
|---|---|
| `CODECOV_TOKEN` | Codecov upload token |
| `GITHUB_TOKEN` | Auto-provided by GitHub Actions |

## Coverage Reports

Coverage is uploaded to [Codecov](https://codecov.io) for each test job,
tagged with flags (`api`, `integration`, `e2e`).

## Allure Reports

Allure results are uploaded as artifacts and published to GitHub Pages
after every successful run on `main`. The report is available at:

```
https://<user>.github.io/petstore-test-python/
```
