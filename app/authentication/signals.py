from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver

from authentication.services import send_verification

User = get_user_model()


@receiver(post_save, sender=User)
def user_registered(sender, **kwargs):
    """
    User registered
    """
    user = kwargs.get('instance')
    created = kwargs.get('created')

    if created and not user.is_superuser:
        send_verification(user)
