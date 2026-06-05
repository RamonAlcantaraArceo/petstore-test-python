"""Fluent assertion helpers.

Provides a readable, chainable assertion DSL on top of plain ``assert``
so that test failures carry descriptive messages.

Example
-------
::

    from framework.assertions import assert_that

    assert_that(response.status_code).equals(200)
    assert_that(pets).is_not_empty().has_length_greater_than(0)
    assert_that(pet["name"]).contains("Fido").starts_with("F")
"""

from __future__ import annotations

from typing import Any, TypeVar

T = TypeVar("T")


class FluentAssertion[T]:
    """Chainable assertion wrapper.

    Instantiate via :func:`assert_that` rather than directly.
    """

    def __init__(self, value: T, description: str = "") -> None:
        self._value = value
        self._desc = description or repr(value)

    # ------------------------------------------------------------------
    # Generic
    # ------------------------------------------------------------------

    def equals(self, expected: Any) -> FluentAssertion[T]:
        """Assert *value* == *expected*."""
        assert (
            self._value == expected
        ), f"Expected {self._desc} to equal {expected!r}, but got {self._value!r}"
        return self

    def not_equals(self, unexpected: Any) -> FluentAssertion[T]:
        """Assert *value* != *unexpected*."""
        assert (
            self._value != unexpected
        ), f"Expected {self._desc} not to equal {unexpected!r}"
        return self

    def is_none(self) -> FluentAssertion[T]:
        """Assert *value* is ``None``."""
        assert (
            self._value is None
        ), f"Expected {self._desc} to be None, got {self._value!r}"
        return self

    def is_not_none(self) -> FluentAssertion[T]:
        """Assert *value* is not ``None``."""
        assert self._value is not None, f"Expected {self._desc} not to be None"
        return self

    def is_true(self) -> FluentAssertion[T]:
        """Assert *value* is truthy."""
        assert self._value, f"Expected {self._desc} to be truthy, got {self._value!r}"
        return self

    def is_false(self) -> FluentAssertion[T]:
        """Assert *value* is falsy."""
        assert (
            not self._value
        ), f"Expected {self._desc} to be falsy, got {self._value!r}"
        return self

    def is_instance_of(self, type_: type) -> FluentAssertion[T]:
        """Assert *value* is an instance of *type_*."""
        assert isinstance(self._value, type_), (
            f"Expected {self._desc} to be instance of {type_.__name__}, "
            f"got {type(self._value).__name__}"
        )
        return self

    # ------------------------------------------------------------------
    # Comparison
    # ------------------------------------------------------------------

    def is_greater_than(self, other: Any) -> FluentAssertion[T]:
        assert (
            self._value > other
        ), f"Expected {self._desc} > {other!r}, got {self._value!r}"
        return self

    def is_less_than(self, other: Any) -> FluentAssertion[T]:
        assert (
            self._value < other
        ), f"Expected {self._desc} < {other!r}, got {self._value!r}"
        return self

    def is_greater_than_or_equal_to(self, other: Any) -> FluentAssertion[T]:
        assert (
            self._value >= other
        ), f"Expected {self._desc} >= {other!r}, got {self._value!r}"
        return self

    def is_less_than_or_equal_to(self, other: Any) -> FluentAssertion[T]:
        assert (
            self._value <= other
        ), f"Expected {self._desc} <= {other!r}, got {self._value!r}"
        return self

    # ------------------------------------------------------------------
    # String
    # ------------------------------------------------------------------

    def contains(self, substring: str) -> FluentAssertion[T]:
        """Assert the string *value* contains *substring*."""
        assert isinstance(
            self._value, str
        ), f"Expected a string, got {type(self._value)}"
        assert (
            substring in self._value
        ), f"Expected {self._desc} to contain {substring!r}"
        return self

    def starts_with(self, prefix: str) -> FluentAssertion[T]:
        assert isinstance(
            self._value, str
        ), f"Expected a string, got {type(self._value)}"
        assert self._value.startswith(
            prefix
        ), f"Expected {self._desc} to start with {prefix!r}"
        return self

    def ends_with(self, suffix: str) -> FluentAssertion[T]:
        assert isinstance(
            self._value, str
        ), f"Expected a string, got {type(self._value)}"
        assert self._value.endswith(
            suffix
        ), f"Expected {self._desc} to end with {suffix!r}"
        return self

    def matches_pattern(self, pattern: str) -> FluentAssertion[T]:
        """Assert the string *value* matches the regex *pattern*."""
        __tracebackhide__ = True
        import re

        assert isinstance(
            self._value, str
        ), f"Expected a string, got {type(self._value)}"
        assert re.search(
            pattern, self._value
        ), f"Expected {self._desc} to match pattern {pattern!r}"
        return self

    # ------------------------------------------------------------------
    # Collections
    # ------------------------------------------------------------------

    def is_empty(self) -> FluentAssertion[T]:
        """Assert the sequence / mapping is empty."""
        assert len(self._value) == 0, (  # type: ignore[arg-type]
            f"Expected {self._desc} to be empty, got length {len(self._value)}"  # type: ignore[arg-type]
        )
        return self

    def is_not_empty(self) -> FluentAssertion[T]:
        """Assert the sequence / mapping is NOT empty."""
        assert len(self._value) > 0, (  # type: ignore[arg-type]
            f"Expected {self._desc} not to be empty"
        )
        return self

    def has_length(self, length: int) -> FluentAssertion[T]:
        actual = len(self._value)  # type: ignore[arg-type]
        assert (
            actual == length
        ), f"Expected {self._desc} to have length {length}, got {actual}"
        return self

    def has_length_greater_than(self, length: int) -> FluentAssertion[T]:
        actual = len(self._value)  # type: ignore[arg-type]
        assert (
            actual > length
        ), f"Expected {self._desc} to have length > {length}, got {actual}"
        return self

    def contains_item(self, item: Any) -> FluentAssertion[T]:
        """Assert *item* is in the collection."""
        assert item in self._value, (  # type: ignore[operator]
            f"Expected {self._desc} to contain {item!r}"
        )
        return self

    # ------------------------------------------------------------------
    # Dict / mapping
    # ------------------------------------------------------------------

    def has_key(self, key: str) -> FluentAssertion[T]:
        """Assert the dict *value* has *key*."""
        assert key in self._value, (  # type: ignore[operator]
            f"Expected {self._desc} to have key {key!r}"
        )
        return self

    def has_keys(self, *keys: str) -> FluentAssertion[T]:
        for key in keys:
            self.has_key(key)
        return self

    def key_value_equals(self, key: str, expected: Any) -> FluentAssertion[T]:
        """Assert ``value[key] == expected``."""
        self.has_key(key)
        actual = self._value[key]  # type: ignore[index]
        assert (
            actual == expected
        ), f"Expected {self._desc}[{key!r}] == {expected!r}, got {actual!r}"
        return self


# ---------------------------------------------------------------------------
# HTTP-specific helper built on top of FluentAssertion
# ---------------------------------------------------------------------------


class ResponseAssertion:
    """Fluent assertions tailored for ``requests.Response`` objects."""

    def __init__(self, response: Any) -> None:
        self._response = response

    def has_status(self, code: int) -> ResponseAssertion:
        actual = self._response.status_code
        assert (
            actual == code
        ), f"Expected HTTP {code}, got {actual}. Body: {self._response.text[:200]}"
        return self

    def is_ok(self) -> ResponseAssertion:
        return self.has_status(200)

    def is_created(self) -> ResponseAssertion:
        return self.has_status(201)

    def is_client_error(self) -> ResponseAssertion:
        """Assert response is a 4xx client error."""
        actual = self._response.status_code
        assert (
            400 <= actual < 500
        ), f"Expected HTTP 4xx client error, got {actual}. Body: {self._response.text[:200]}"
        return self
    
    def is_bad_request(self) -> ResponseAssertion:
        return self.has_status(400)

    def is_unauthorized(self) -> ResponseAssertion:
        return self.has_status(401)

    def is_not_found(self) -> ResponseAssertion:
        return self.has_status(404)

    def is_server_error(self) -> ResponseAssertion:
        """Assert response is a 500 server error."""
        actual = self._response.status_code
        assert (
            actual == 500
        ), f"Expected HTTP 500 server error, got {actual}. Body: {self._response.text[:200]}"

        return self

    def body_contains(self, text: str) -> ResponseAssertion:
        assert text in self._response.text, (
            f"Expected response body to contain {text!r}. "
            f"Actual body: {self._response.text[:300]}"
        )
        return self

    def json_has_key(self, key: str) -> ResponseAssertion:
        __tracebackhide__ = True
        data = self._response.json()
        assert (
            key in data
        ), f"Expected JSON body to have key {key!r}. Got keys: {list(data)}"
        return self

    def json_key_equals(self, key: str, expected: Any) -> ResponseAssertion:
        data = self._response.json()
        assert (
            data.get(key) == expected
        ), f"Expected JSON[{key!r}] == {expected!r}, got {data.get(key)!r}"
        return self


# ---------------------------------------------------------------------------
# Public factory helpers
# ---------------------------------------------------------------------------


def assert_that[T](value: T, description: str = "") -> FluentAssertion[T]:
    """Entry point for fluent assertions.

    Example
    -------
    ::

        assert_that(pet["name"]).equals("Fido")
        assert_that(pets).is_not_empty()
    """
    return FluentAssertion(value, description)


def assert_response(response: Any) -> ResponseAssertion:
    """Entry point for fluent HTTP response assertions.

    Example
    -------
    ::

        assert_response(resp).is_ok().json_has_key("id")
    """
    return ResponseAssertion(response)


# ---------------------------------------------------------------------------
# DB-record assertions
# ---------------------------------------------------------------------------


class DbRecordAssertion:
    """Fluent assertions for a single database row returned as a dict.

    Instantiate via :func:`assert_db_record` rather than directly.

    Example
    -------
    ::

        row = db_client.get_pet(pet_id)
        assert_db_record(row).exists().field_equals("name", "Fido").field_in("status", ["available", "pending"])
    """

    def __init__(self, record: dict[str, Any] | None) -> None:
        self._record = record

    def exists(self) -> DbRecordAssertion:
        """Assert the record was found in the database (is not ``None``)."""
        assert self._record is not None, "Expected a DB record to exist, but got None"
        return self

    def is_deleted(self) -> DbRecordAssertion:
        """Assert the record was *not* found (has been deleted)."""
        assert self._record is None, (
            f"Expected DB record to be deleted, but found: {self._record!r}"
        )
        return self

    def field_equals(self, field: str, expected: Any) -> DbRecordAssertion:
        """Assert ``record[field] == expected``."""
        self.exists()
        actual = self._record[field]  # type: ignore[index]
        assert actual == expected, (
            f"Expected DB record field {field!r} == {expected!r}, got {actual!r}"
        )
        return self

    def field_not_equals(self, field: str, unexpected: Any) -> DbRecordAssertion:
        """Assert ``record[field] != unexpected``."""
        self.exists()
        actual = self._record[field]  # type: ignore[index]
        assert actual != unexpected, (
            f"Expected DB record field {field!r} != {unexpected!r}, but it was equal"
        )
        return self

    def field_is_not_none(self, field: str) -> DbRecordAssertion:
        """Assert ``record[field]`` is not ``None``."""
        self.exists()
        actual = self._record[field]  # type: ignore[index]
        assert actual is not None, (
            f"Expected DB record field {field!r} to be non-None"
        )
        return self

    def field_is_none(self, field: str) -> DbRecordAssertion:
        """Assert ``record[field]`` is ``None``."""
        self.exists()
        actual = self._record[field]  # type: ignore[index]
        assert actual is None, (
            f"Expected DB record field {field!r} to be None, got {actual!r}"
        )
        return self

    def field_in(self, field: str, allowed: list[Any]) -> DbRecordAssertion:
        """Assert ``record[field]`` is one of the *allowed* values."""
        self.exists()
        actual = self._record[field]  # type: ignore[index]
        assert actual in allowed, (
            f"Expected DB record field {field!r} to be one of {allowed!r}, got {actual!r}"
        )
        return self

    def has_field(self, field: str) -> DbRecordAssertion:
        """Assert the record dict contains *field* as a key."""
        self.exists()
        assert field in self._record, (  # type: ignore[operator]
            f"Expected DB record to have field {field!r}. Keys: {list(self._record)}"  # type: ignore[arg-type]
        )
        return self


def assert_db_record(record: dict[str, Any] | None) -> DbRecordAssertion:
    """Entry point for fluent DB record assertions.

    Example
    -------
    ::

        assert_db_record(db_client.get_pet(pet_id)).exists().field_equals("name", "Fido")
        assert_db_record(db_client.get_pet(deleted_id)).is_deleted()
    """
    return DbRecordAssertion(record)
