"""Public functions for Clients app"""
import logging

from django.db import connections
from django.conf import settings
from django.db.utils import OperationalError

from core import functions as cf


logger = logging.getLogger('errors')


def get_client_by_uid(uid, fields):
    """Return selected fields for client by AWS UID"""
    uid = (uid or '').strip()
    if uid == '' or not isinstance(fields, list) or not fields:
        return
    sql = 'SELECT {fields} FROM members_user WHERE uid=%s LIMIT 1'\
        .format(fields=', '.join(fields))
    return _sql_select(sql, [uid], fields)


def get_client_by_id(pk, fields):
    """Return selected fields for client by Deal ID"""
    pk = cf.get_int_or_none(pk)
    if pk is None or not isinstance(fields, list) or not fields:
        return
    sql = 'SELECT {fields} FROM members_user WHERE bitrix_id=%s LIMIT 1'\
        .format(fields=', '.join(fields))
    return _sql_select(sql, [pk], fields)


def get_client_by_lead_id(pk, fields):
    """Return selected fields for client by Lead ID"""
    pk = cf.get_int_or_none(pk)
    if pk is None or not isinstance(fields, list) or not fields:
        return
    sql = 'SELECT {fields} FROM members_user WHERE bitrix_lead=%s LIMIT 1'\
        .format(fields=', '.join(fields))
    return _sql_select(sql, [pk], fields)


def _sql_select(sql, payload, fields, many=False):
    """Execute given SELECT SQL"""
    try:
        cursor = connections['second'].cursor()
        cursor.execute(sql, payload)
        if cursor.rowcount < 1:
            return

        if many is False:
            return _map_result_data(fields, cursor.fetchone(), many)
        else:
            return _map_result_data(fields, cursor.fetchall(), many)

    except OperationalError as err:
        logger.error('ERROR: %s. SQL: %s. DATA: %s', err, sql, payload)


def _map_result_data(fields, data, many=False):
    """Map list of field values to dictionary"""
    if data is None or not data:
        return None
    try:
        if many is True:
            result = []
            for record in data:
                _record = {}
                for num, name in enumerate(fields):
                    _record[name] = record[num]
                result.append(_record)
            return result
        else:
            result = {}
            for num, name in enumerate(fields):
                result[name] = data[num]
            return result
    except IndexError:
        logger.error('Error map SQL result. Fields: %s. Data: %s', fields,
                     data)
    return None
