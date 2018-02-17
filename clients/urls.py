"""Router for Clients app"""
from django.urls import path

from . import views


app_name = 'clients'

urlpatterns = [
    path('<uid>/validate/phone', views.validate_phone_view,
         name='validate-phone'),
    path('<uid>/validate/email', views.validate_email_view,
         name='validate-email'),
    path('<uid>/verified/internal', views.internal_verify_view,
         name='verify-internal'),
    path('<uid>/verified/bank', views.bank_verify_view,
         name='verify-bank'),
]
