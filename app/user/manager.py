from django.contrib.auth.models import BaseUserManager
from django.db import transaction

from core.utils import timezone


class UserManager(BaseUserManager):
    """User model manager"""

    def create_user(self, first_name, last_name, email, password=None,
                    **kwargs):
        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=email,
            **kwargs
        )

        if password:
            user.set_password(password)

        user.save(using=self._db)

        return user

    @transaction.atomic()
    def create_superuser(self, first_name, last_name, email, password):
        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=email,
        )
        user.set_password(password)
        user.is_superuser = True
        user.verified_at = timezone.now()
        user.save(using=self._db)

        return user
