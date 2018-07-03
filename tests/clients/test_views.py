from clients.views import *
from core.helpers import get_logged_user
import pytest

from django.http.request import HttpRequest


rq = HttpRequest()

@pytest.mark.django_db(transaction=False)
def test_validate_phone_view():
  assert validate_phone_view(rq, '') == 'Wrong Client UID:'