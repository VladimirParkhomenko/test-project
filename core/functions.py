# coding: utf-8
"""Core functions for project"""
import datetime
import json
import re

from collections import OrderedDict
from decimal import Decimal, InvalidOperation

from rest_framework.response import Response

from django.conf import settings
from django.shortcuts import _get_queryset
from django.utils.crypto import get_random_string


def make_random_string(length=10, prefix=''):
    """Generates a random string with the given length"""
    allowed_chars = 'abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'
    length -= len(prefix or '')
    return prefix + get_random_string(length, allowed_chars)


def get_config(key, default=None):
    """
    Get settings from django.conf if exists,
    return default value otherwise

    example:

    ADMIN_EMAIL = get_config('ADMIN_EMAIL', 'default@email.com')
    """
    return getattr(settings, key, default)


def get_form_errors(form, as_str=False):
    """Return form errors for API response"""
    errors = {}
    for field, messages in sorted(form.errors.items()):
        errors[field] = u' '.join(messages)
    if as_str:
        return u' '.join([u'{}: {}'.format(name, value)
                          for name, value in sorted(errors.items())])
    return errors


def error_response(error, status=400):
    """Return API Response with error"""
    return Response({'result': 'error', 'error': error}, status=status)


def success_response(token=None, data=None, ttl=None):
    """Return success API Response"""
    if ttl is None or not isinstance(ttl, int):
        ttl = get_config('DEFAULT_DATA_TTL', 0)
    result = OrderedDict([
        ('status', 'OK'),
        ('ttl', ttl),
    ])
    if token is not None:
        result['Token'] = token
    if data is not None:
        result['payload'] = data
    return Response(result)


def get_object_or_none(klass, *args, **kwargs):
    """
    Uses get() to return an object or None if the object does not exist.

    klass may be a Model, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the get() query.

    Note: Like with get(), a MultipleObjectsReturned will be raised
        if more than one object is found.
    """
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return None


def get_int_or_none(value):
    """Return value as Integer or None"""
    try:
        return int(value)
    except (TypeError, ValueError):
        pass


def get_decimal_or_none(value):
    """Return value as Decimal or None"""
    try:
        return Decimal(str(value))
    except (TypeError, ValueError, InvalidOperation):
        pass


def get_datetime_or_none(value, date_format="%Y-%m-%d"):
    try:
        return datetime.datetime.strptime(value, date_format)
    except (TypeError, ValueError, AttributeError):
        pass


def get_date_or_none(value, date_format="%Y-%m-%d"):
    try:
        return datetime.datetime.strptime(value, date_format).date()
    except (TypeError, ValueError, AttributeError):
        pass


def to_json(data):
    """Prepare data for assertion with JSON response"""
    return json.dumps(data, separators=(',', ':'))


def prepare_dict_for_json(data):
    """Convert all items of dictionaty to string"""
    for key, value in data.items():
        if isinstance(value, dict):
            data[key] = prepare_dict_for_json(value)
        elif not isinstance(value, list) and not isinstance(value, tuple):
            data[key] = str(value)
    return data
