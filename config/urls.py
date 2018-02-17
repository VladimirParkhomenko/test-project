"""Main Routers"""
from django.urls import include, path

urlpatterns = [
    path('api/1.0/client/', include('clients.urls')),
]
