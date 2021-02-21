from datetime import date

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _

from core.abstract_models import TimestampMixin
from .manager import UserManager
from .options.constants import (
    USER_ROLE_CHOICES,
    USER_ROLE_FAM_MEMBER
)


class User(AbstractBaseUser, PermissionsMixin, TimestampMixin):
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
        unique=True,
        null=True,
        blank=True,
    )
    username = models.CharField(
        _('Username'),
        max_length=255,
        unique=True
    )
    verified_at = models.DateTimeField(
        null=True,
        blank=True
    )
    role = models.CharField(
        _('User role'),
        max_length=255,
        choices=USER_ROLE_CHOICES,
        default=USER_ROLE_FAM_MEMBER
    )
    family = models.ForeignKey(
        'Family',
        on_delete=models.CASCADE,
        related_name='family_members',
        verbose_name=_('Family'),
        null=True,
        blank=True
    )
    d_o_b = models.DateField(
        _('Date of birth'),
        null=True,
        blank=True
    )
    photo = models.ImageField(
        _('Profile image'),
        upload_to='profiles',
        null=True,
        blank=True
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ('first_name', 'last_name')

    objects = UserManager()

    class Meta:
        ordering = ('created_at',)
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.username

    @property
    def is_staff(self):
        return self.is_superuser

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def role_text(self):
        return self.get_role_display()

    @property
    def age(self):
        if self.d_o_b:
            today = date.today()
            born = self.d_o_b

            return today.year - born.year


class Family(TimestampMixin):
    """Family model"""
    name = models.CharField(
        _('Family name'),
        max_length=255
    )
    photo = models.ImageField(
        _('Family photo'),
        upload_to='family_photos',
        null=True,
        blank=True
    )
    region = models.CharField(
        _('Region'),
        max_length=255,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = _('Family')
        verbose_name_plural = _('Families')

    def __str__(self):
        return self.name
