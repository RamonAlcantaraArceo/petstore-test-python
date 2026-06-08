"""Test-data factories using factory_boy and Faker.

Usage
-----
::

    from framework.factories import PetFactory, UserFactory

    pet_data = PetFactory.build()          # dict (no network call)
    pet_data = PetFactory.build(name="Rex")

    user_data = UserFactory.build()
"""

from __future__ import annotations

from factory import DictFactory, Iterator, LazyAttribute, LazyFunction
from faker import Faker

fake = Faker()


class PetFactory(DictFactory):
    """Generate pet payloads compatible with the Petstore API."""

    id = LazyFunction(lambda: fake.random_int(min=1_000_000, max=9_999_999))
    name = LazyFunction(fake.first_name)
    photoUrls = LazyFunction(lambda: [fake.image_url()])
    status = Iterator(["available", "pending", "sold"])
    category = LazyFunction(lambda: {"id": fake.random_int(1, 10), "name": fake.word()})
    tags = LazyFunction(lambda: [{"id": fake.random_int(1, 100), "name": fake.word()}])


class UserFactory(DictFactory):
    """Generate user payloads compatible with the Petstore API."""

    id = LazyFunction(lambda: fake.random_int(min=1_000_000, max=9_999_999))
    username = LazyFunction(lambda: fake.user_name() + str(fake.random_int(1, 9999)))
    firstName = LazyFunction(fake.first_name)
    lastName = LazyFunction(fake.last_name)
    email = LazyAttribute(lambda o: f"{o.username}@example.com")
    password = LazyFunction(lambda: fake.password(length=12))
    phone = LazyFunction(fake.phone_number)
    userStatus = 1
