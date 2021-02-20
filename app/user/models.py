from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _

from core.abstract_models import TimestampAbstractModel
from .manager import UserManager


class User(AbstractBaseUser, PermissionsMixin, TimestampAbstractModel):
    """Base user abstract class override"""
    first_name = models.CharField(
        _('First name'),
        max_length=255
    )
    last_name = models.CharField(
        _('Last name'),
        max_length=255
    )
    email = models.EmailField(
        _('Email'),
        max_length=255,
        unique=True
    )
    verified_at = models.DateTimeField(
        null=True,
        blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name')

    objects = UserManager()

    class Meta:
        ordering = ('created_at',)
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_superuser

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
