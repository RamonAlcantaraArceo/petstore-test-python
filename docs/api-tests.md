# API Tests

API tests send real HTTP requests to the Petstore REST API using the
[requests](https://requests.readthedocs.io/) library.

## Location

```
tests/api/
├── conftest.py       # API-specific fixtures (new_pet, etc.)
├── test_login.py     # Authentication tests
└── test_pets.py      # Pet CRUD tests
```

## Running

```bash
uv run pytest tests/api/ -m api -v
```

## Example: Login

```python
from framework.assertions import assert_that, assert_response

def test_login_sets_authenticated_state(api_client):
    assert_that(api_client.is_logged_in()).is_false()

    api_client.login("user1", "password1")

    assert_that(api_client.is_logged_in()).is_true()
```

## Example: Pet CRUD

```python
def test_add_pet_returns_created_pet(api_client):
    pet = api_client.add_pet(name="Fido", status="available", photoUrls=[])

    assert_that(pet).has_keys("id", "name", "status")
    assert_that(pet["name"]).equals("Fido")
    assert_that(pet["status"]).equals("available")

    api_client.delete_pet(pet["id"])
```

## Raw Response Assertions

```python
def test_get_nonexistent_pet(api_client):
    response = api_client.raw_get("/pet/999999999999")
    assert_response(response).is_not_found()
```

## API Client Reference

::: framework.api_client.PetstoreApiClient
