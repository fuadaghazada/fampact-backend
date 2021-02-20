from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver

from .models import Family

User = get_user_model()


@receiver(post_save, sender=User)
def create_family(sender, **kwargs):
    """
    User registered: create family
    """
    user = kwargs.get('instance')
    created = kwargs.get('created')

    if created and not user.is_superuser and not user.family:
        family = Family.objects.create(
            name=user.last_name
        )
        user.family = family
        user.save()
