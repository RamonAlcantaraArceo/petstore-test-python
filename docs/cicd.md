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

Allure results are collected per suite job using `--alluredir` and uploaded as
artifacts. After all suites complete (on `main` only) the `allure-report` job:

1. Downloads and merges all `allure-results-*` artifacts.
2. Restores historical trend data from the `gh-pages` branch
   (`gh-pages/history/` → `allure-results/history/`).
3. Runs **Allure 3 CLI** (`allure-commandline` npm package) to generate a
   static HTML report:
   ```bash
   allure generate --clean allure-results -o allure-report
   ```
4. Publishes the generated `allure-report/` directory to the `gh-pages` branch
   via `peaceiris/actions-gh-pages`.

The published report is available at:

```
https://<user>.github.io/petstore-test-python/
```

### Local Allure 3 report generation

```bash
# Run any suite to collect results
uv run pytest tests/api/ --alluredir=allure-results

# Generate report (requires Node.js)
npx allure-commandline generate --clean allure-results -o allure-report

# Open report
npx allure-commandline open allure-report
```
