"""Actions for Clients app"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.db import connections

from core import functions as cf
from . import api


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def validate_phone_view(request, uid):
    """
    Request for initialize phone confirmation.

    Input:
    {}

    Return:
    {
        result: "ok"
    }
    or error:
    {
        result: "error",
        error: "description"
    }
    """
    uid = (uid or '').strip()
    if uid == '':
        return cf.error_response('Wrong Client UID: {}'.format(uid))
    user = api.get_client_by_uid(uid, ['id', 'verify_phone'])
    if user is None:
        return cf.error_response('Client is not found', status=404)
    if cf.get_int_or_none(user['verify_phone']) == 1:
        return cf.error_response('Client has verified phone', status=400)

    print('Request validate phone for Client UID:', uid)

    return Response({'result': 'ok'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def validate_email_view(request, uid):
    """
    Request for initialize email confirmation.

    Input:
    {}

    Return:
    {
        result: "ok"
    }
    or error:
    {
        result: "error",
        error: "description"
    }
    """
    uid = (uid or '').strip()
    if uid == '':
        return cf.error_response('Wrong Client UID: {}'.format(uid))
    if api.get_client_by_uid(uid, ['id']) is None:
        return cf.error_response('Client is not found', status=404)

    print('Request validate email for Client UID:', uid)

    return Response({'result': 'ok'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def internal_verify_view(request, uid):
    """
    Request for setting result of Internal Verification.

    Input:
    {
        status: "ok",  // "blacklist", "again"
        comment: "comment",
        required_docs: ["doc1", "doc2"]  // if status=again
    }

    Return:
    {
        result: "ok",
        bank_dept_id: 12
    }
    or error:
    {
        result: "error",
        error: "description"
    }
    """
    status = (request.data.get('status') or '').strip().lower()
    if status == '':
        return cf.error_response('Missed input: status')

    uid = (uid or '').strip()
    if uid == '':
        return cf.error_response('Wrong Client UID: {}'.format(uid))
    if api.get_client_by_uid(uid, ['id']) is None:
        return cf.error_response('Client is not found', status=404)

    comment = (request.data.get('comment') or '').strip()

    if status == 'ok':
        print('Internal verification passed with status:', status)
        return Response({
            'result': 'ok',
            'bank_dept_id': cf.get_config('DEPARTMENT_BANK')
        })

    if status == 'blacklist':
        print('Internal verification passed with status:', status)
        return Response({'result': 'ok'})

    if status == 'again':
        if 'required_docs' not in request.data or \
                request.data['required_docs'] is None or \
                not request.data['required_docs']:
            return cf.error_response('Missed input: required_docs')
        docs = request.data['required_docs']

        print('Internal verification passed with status:', status)
        return Response({'result': 'ok'})

    return cf.error_response('Unknown status: {}'.format(status))


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def bank_verify_view(request, uid):
    """
    Request for setting result of Bank Verification.

    Input:
    {
        status: "ok",  // "blacklist", "again"
        comment: "comment",
        required_docs: ["doc1", "doc2"]  // if status=again
    }

    Return:
    {
        result: "ok"
    }
    or error:
    {
        result: "error",
        error: "description"
    }
    """
    status = (request.data.get('status') or '').strip().lower()
    if status == '':
        return cf.error_response('Missed input: status')

    uid = (uid or '').strip()
    if uid == '':
        return cf.error_response('Wrong Client UID: {}'.format(uid))
    if api.get_client_by_uid(uid, ['id']) is None:
        return cf.error_response('Client is not found', status=404)

    comment = (request.data.get('comment') or '').strip()

    if status == 'ok':
        print('Bank verification passed with status:', status)
        return Response({'result': 'ok'})

    if status == 'blacklist':
        print('Bank verification passed with status:', status)
        return Response({'result': 'ok'})

    if status == 'again':
        if 'required_docs' not in request.data or \
                request.data['required_docs'] is None or \
                not request.data['required_docs']:
            return cf.error_response('Missed input: required_docs')
        docs = request.data['required_docs']

        print('Bank verification passed with status:', status)
        return Response({'result': 'ok'})

    return cf.error_response('Unknown status: {}'.format(status))
