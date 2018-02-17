# coding: utf-8
"""Helpers for testing"""
from rest_framework.authtoken.models import Token

from users.tests.helpers import UserFactory


def get_logged_user(uid=None):
    """Return user and token for authorization"""
    user = UserFactory(is_active=True, uid=uid)
    token = Token.objects.create(user=user)
    return (user, token.key)
