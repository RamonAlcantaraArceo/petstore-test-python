# End-to-End Tests

E2E tests exercise complete user journeys from start to finish, verifying
that the system behaves correctly at the highest level.

## Location

```
tests/e2e/
└── test_pet_lifecycle.py    # Full adoption + user registration journeys
```

## Running

```bash
uv run pytest tests/e2e/ -m e2e -v
```

## Example: Pet Adoption Journey

```python
def test_available_pet_can_be_marked_as_sold(api_client):
    pet = api_client.add_pet(name="AdoptMe", status="available", photoUrls=[])

    # Verify it appears in 'available' list
    available = api_client.find_pets_by_status("available")
    assert_that(any(p["id"] == pet["id"] for p in available)).is_true()

    # 'Purchase' the pet
    api_client.update_pet(pet["id"], status="sold")

    # Verify it moved to 'sold'
    sold = api_client.find_pets_by_status("sold")
    assert_that(any(p["id"] == pet["id"] for p in sold)).is_true()

    api_client.delete_pet(pet["id"])
```
