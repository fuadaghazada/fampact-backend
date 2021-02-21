from django.contrib.auth.models import BaseUserManager
from django.db import transaction

from core.utils import timezone
from user.options.constants import (
    USER_ROLE_ADMIN,
    USER_ROLE_PARENT,
    USER_ROLE_CHILD
)


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
    def create_superuser(self, first_name, last_name, username, password):
        user = self.model(
            first_name=first_name,
            last_name=last_name,
            username=username,
        )
        user.set_password(password)
        user.is_superuser = True
        user.role = USER_ROLE_ADMIN
        user.verified_at = timezone.now()
        user.save(using=self._db)

        return user

    def add_member(self, first_name, email, adder):
        user = self.model(
            first_name=first_name,
            last_name=adder.family.name,
            email=email,
            family=adder.family
        )
        user.save(using=self._db)

        return user

    def add_child(self, first_name, username, password, adder):
        user = self.model(
            first_name=first_name,
            last_name=adder.family.name,
            username=username,
            family=adder.family
        )
        user.role = USER_ROLE_CHILD
        user.set_password(password)
        user.verified_at = timezone.now()
        user.save()

        adder.role = USER_ROLE_PARENT
        adder.save()

        return user
