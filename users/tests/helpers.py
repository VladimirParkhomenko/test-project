# coding: utf-8
"""Helper factories for tests"""
import factory.fuzzy

from factory_djoy import CleanModelFactory
from faker import Faker

from ..models import User


class UserFactory(CleanModelFactory):
    username = factory.fuzzy.FuzzyText(length=12)
    phone = Faker().phone_number()
    password = Faker().md5(raw_output=False)

    class Meta:
        model = User
