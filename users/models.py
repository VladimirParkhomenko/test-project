"""Models for Users"""
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

from core.db import UpdatableMixin


class User(UpdatableMixin, AbstractUser):
    """Model for Operator"""

    uid = models.CharField(max_length=250, blank=True, null=True,
                           db_index=True)
    phone = models.CharField(max_length=50)
    aws_group = models.CharField(max_length=25, blank=True, null=True)

    # Status
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'users'

    class UpdateMeta:
        allowed_fields = ('is_active', 'email', 'phone', 'first_name',
                          'last_name', 'aws_group')

    def __unicode__(self):
        return self.get_full_name()

    def delete(self, **kwargs):
        self.is_deleted = True
        self.save()
