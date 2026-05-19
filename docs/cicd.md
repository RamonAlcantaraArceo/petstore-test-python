# CI/CD

The repository uses **GitHub Actions** for automated testing and deployment.

## Workflows

### `ci.yml` – Main CI Pipeline

Triggered on every push and pull request to `main`.

| Job                 | Description                                  |
|---------------------|----------------------------------------------|
| `lint`              | ruff, black (format check), mypy             |
| `api-tests`         | Runs `tests/api/` with coverage              |
| `integration-tests` | Runs `tests/integration/` with coverage      |
| `e2e-tests`         | Runs `tests/e2e/` with coverage              |
| `ui-tests`          | Runs `tests/ui/` with headless Chrome        |
| `allure-report`     | Merges results and publishes to GitHub Pages |

### `docs.yml` – Documentation Deployment

Triggered on pushes to `main` that touch `docs/` or `mkdocs.yml`.
Builds MkDocs and deploys to the `gh-pages` branch.

## Secrets

Configure these in **Settings → Secrets and variables → Actions**:

| Secret          | Description                     |
|-----------------|---------------------------------|
| `CODECOV_TOKEN` | Codecov upload token            |
| `GITHUB_TOKEN`  | Auto-provided by GitHub Actions |

## Coverage Reports

Coverage is uploaded to [Codecov](https://codecov.io) for each test job,
tagged with flags (`api`, `integration`, `e2e`).

## Allure Reports

Allure results are collected per suite job using `--alluredir` and uploaded as
artifacts. After all suites complete the `allure-report` job:

1. Downloads and merges all `allure-results-*` artifacts.
2. Restores the Allure 3 JSONL history file from the `gh-pages` branch
   (stored at `<report-subpath>/.allure/allure-history.jsonl`).
3. Runs **Allure 3 CLI** to generate a static HTML report, using the
   `historyPath` set in `allurerc.yml`.
4. Copies the updated JSONL file back into the report output directory so it
   is published alongside the HTML.
5. Publishes the report directory to the `gh-pages` branch via
   `peaceiris/actions-gh-pages`.

The published report is available at:

```
https://<owner>.github.io/<repo>/<report-subpath>/
```

### Allure 3 history — `allurerc.yml` requirement

Allure 3 only writes the cross-build history JSONL file when `historyPath` is
configured. The reusable workflow reads this from an `allurerc.yml` file in the
**calling repository's root** (auto-discovered by the Allure CLI from CWD).

**Every repository that calls the reusable workflow must have an `allurerc.yml`
at its root**, containing at minimum:

```yaml
name: "My Report Name"
historyPath: "./.allure/allure-history.jsonl"
appendHistory: true
```

Without this file the `allure generate` step will not write the JSONL, no
history is persisted to `gh-pages`, and trend charts will remain empty.

### Local Allure 3 report generation

```bash
# Run any suite to collect results
uv run pytest tests/api/ -p allure_pytest --alluredir=allure-results

# Generate report locally (Allure 3 CLI required)
allure generate allure-results --output allure-report

# Open report in browser
allure open allure-report
```

## Reusable Workflows and Actions

This repository publishes a reusable workflow and three composite actions that
any repository in the same GitHub account can consume.

---

### Reusable workflow — `allure-report.yml`

The primary entry point for Allure reporting. Downloads uploaded result
artifacts, injects executor metadata, and delegates to the
`publish-allure-ci-history` composite action.

```yaml
# In your repo's CI workflow
allure-report:
  name: Publish Allure Report
  needs: [test]          # wait for jobs that upload allure-results artifacts
  if: always()
  permissions:
    contents: write
    pages: write
    id-token: write
    pull-requests: write
    checks: write
  uses: RamonAlcantaraArceo/petstore-test-python/.github/workflows/allure-report.yml@main
  with:
    artifact-pattern: "allure-results"   # glob matching uploaded artifact names
    report-subpath: "ci"                 # subdirectory on gh-pages
    allure-report-name: "My Test Report"
    publish-report: true
  secrets:
    GH_PAGES_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

Workflow inputs:

| Input                | Description                                           | Default            |
|----------------------|-------------------------------------------------------|--------------------|
| `allure-report-name` | Display name embedded in executor metadata            | required           |
| `artifact-pattern`   | Glob matching uploaded Allure result artifact names   | `allure-results-*` |
| `allure-config`      | Path to `allurerc.yml` in the calling repo            | `allurerc.yml`     |
| `history-limit`      | Maximum history entries to retain in trend charts     | `20`               |
| `report-subpath`     | Subdirectory under the published site for this report | `""` (root)        |
| `publish-report`     | Push report to `gh-pages`                             | `true`             |

> **Prerequisite:** the calling repository must have `allurerc.yml` at its root
> with `historyPath` set. See [Allure 3 history](#allure-3-history--allurercyml-requirement).

---

### Composite action — `setup-env`

Installs Node.js, Python, `uv`, project dependencies, and optionally Chrome
and the Allure CLI. Used as the first step in every job.

```yaml
- name: Setup environment
  uses: RamonAlcantaraArceo/petstore-test-python/.github/actions/setup-env@main
  with:
    python-version: "3.12"
    install-allure: true   # required for the allure-report job
```

Action inputs:

| Input            | Description                   | Default        |
|------------------|-------------------------------|----------------|
| `node-version`   | Node.js version               | `24`           |
| `python-version` | Python version                | `3.12`         |
| `uv-sync-flags`  | Flags forwarded to `uv sync`  | `--all-extras` |
| `install-chrome` | Install Chrome (for UI tests) | `false`        |
| `install-allure` | Install Allure 3 CLI via npm  | `false`        |
| `allure-version` | Allure npm package version    | `latest`       |

---

### Composite action — `upload-results`

Uploads JUnit XML, coverage XML (to Codecov), and Allure result files (as a
GitHub Actions artifact) in a single step.

```yaml
- name: Upload results
  uses: RamonAlcantaraArceo/petstore-test-python/.github/actions/upload-results@main
  with:
    codecov-token: ${{ secrets.CODECOV_TOKEN }}
    junit-file: junit.xml
    coverage-file: coverage.xml
    codecov-flags: api
    allure-results-path: allure-results/
    allure-artifact-name: allure-results
```

Action inputs:

| Input                  | Description                                    |
|------------------------|------------------------------------------------|
| `codecov-token`        | Codecov upload token (required)                |
| `junit-file`           | Path to JUnit XML test results                 |
| `coverage-file`        | Path to coverage XML file                      |
| `codecov-flags`        | Codecov flag for this suite (e.g. `api`, `ui`) |
| `allure-results-path`  | Directory containing Allure result files       |
| `allure-artifact-name` | Artifact name for the uploaded results         |

> The artifact name must match the `artifact-pattern` input of the reusable
> `allure-report.yml` workflow so the results are downloaded correctly.

---

### Composite action — `publish-allure-ci-history`

Low-level building block used by `allure-report.yml`. Use this directly only
when you need more control than the reusable workflow provides (e.g. custom
checkout paths or conditional publishing).

```yaml
- name: Publish CI Allure report with history
  if: always()
  uses: RamonAlcantaraArceo/petstore-test-python/.github/actions/publish-allure-ci-history@main
  with:
    github-token: ${{ secrets.GITHUB_TOKEN }}
    allure-results-path: allure-results
    report-subpath: ci
    allure-config: allurerc.yml
```

Action inputs:

| Input                 | Description                                                    | Default          |
|-----------------------|----------------------------------------------------------------|------------------|
| `github-token`        | Token for gh-pages publish and PR summary                      | required         |
| `allure-results-path` | Directory containing Allure result files                       | `allure-results` |
| `publish-branch`      | Branch used for static report hosting                          | `gh-pages`       |
| `report-subpath`      | Report location under published site                           | `""` (root)      |
| `history-workspace`   | Temp directory used to reconstruct the published site          | `allure-history` |
| `checkout-path`       | Checkout path for the published branch                         | `gh-pages`       |
| `allure-config`       | Path to `allurerc.yml`; skipped if file does not exist         | `""`             |
| `history-limit`       | Number of past builds to keep in trend charts                  | `20`             |
| `publish-report`      | Push report to `gh-pages`                                      | `true`           |
| `post-summary`        | Post Allure summary to PR and job summary                      | `true`           |
| `report-url`          | Explicit report URL; computed from owner/repo/subpath if empty | `""`             |
