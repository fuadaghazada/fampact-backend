from django.utils import timezone


def now():
    """Returns local current date time"""
    return timezone.localtime(timezone.now())
