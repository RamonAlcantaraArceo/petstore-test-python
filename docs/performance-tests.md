# Performance Tests

Performance / benchmark tests use [pytest-benchmark](https://pytest-benchmark.readthedocs.io/)
to measure the speed of key operations.

!!! warning "Manual Only"
    Performance tests are **excluded from CI** and should be run manually
    to avoid flaky results caused by CI runner variability.

## Location

```
tests/performance/
└── test_benchmarks.py
```

## Running

```bash
uv run pytest tests/performance/ --benchmark-only
```

## Comparing Runs

```bash
# Save a baseline
uv run pytest tests/performance/ --benchmark-only --benchmark-save=baseline

# Compare against baseline
uv run pytest tests/performance/ --benchmark-only --benchmark-compare=baseline
```

## Example

```python
def test_find_pets_by_status_speed(benchmark, api_client):
    result = benchmark(api_client.find_pets_by_status, "available")
    assert isinstance(result, list)
```
