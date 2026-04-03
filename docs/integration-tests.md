# Integration Tests

Integration tests verify that multiple components work together correctly,
testing full data round-trips through the API stack.

## Location

```
tests/integration/
└── test_pets.py     # Pet lifecycle + multi-component scenarios
```

## Running

```bash
uv run pytest tests/integration/ -m integration -v
```

## Example

```python
def test_create_read_update_delete_pet(api_client):
    pet = api_client.add_pet(name="IntegrationPet", status="available", photoUrls=[])

    fetched = api_client.get_pet(pet["id"])
    assert_that(fetched["name"]).equals("IntegrationPet")

    updated = api_client.update_pet(pet["id"], status="pending")
    assert_that(updated["status"]).equals("pending")

    api_client.delete_pet(pet["id"])

    response = api_client.raw_get(f"/pet/{pet['id']}")
    assert_that(response.status_code).equals(404)
```
