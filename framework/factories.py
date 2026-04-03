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

import factory
from faker import Faker

fake = Faker()


class PetFactory(factory.DictFactory):
    """Generate pet payloads compatible with the Petstore API."""

    id = factory.LazyFunction(lambda: fake.random_int(min=1_000_000, max=9_999_999))
    name = factory.LazyFunction(fake.first_name)
    photoUrls: list[str] = factory.LazyFunction(lambda: [fake.image_url()])
    status = factory.Iterator(["available", "pending", "sold"])
    category = factory.LazyFunction(
        lambda: {"id": fake.random_int(1, 10), "name": fake.word()}
    )
    tags = factory.LazyFunction(
        lambda: [{"id": fake.random_int(1, 100), "name": fake.word()}]
    )


class UserFactory(factory.DictFactory):
    """Generate user payloads compatible with the Petstore API."""

    id = factory.LazyFunction(lambda: fake.random_int(min=1_000_000, max=9_999_999))
    username = factory.LazyFunction(
        lambda: fake.user_name() + str(fake.random_int(1, 9999))
    )
    firstName = factory.LazyFunction(fake.first_name)
    lastName = factory.LazyFunction(fake.last_name)
    email = factory.LazyAttribute(lambda o: f"{o.username}@example.com")
    password = factory.LazyFunction(lambda: fake.password(length=12))
    phone = factory.LazyFunction(fake.phone_number)
    userStatus = 1
