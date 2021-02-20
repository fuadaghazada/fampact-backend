from django.core.mail import send_mail as mailer

from django.conf import settings


def send_email(subject: str, to_email_list: list, body: str):
    """
        Sending email with the given data
    """
    from_email = settings.DEFAULT_FROM_EMAIL
    mailer(
        subject=subject,
        message=body,
        from_email=from_email,
        recipient_list=to_email_list,
        fail_silently=True
    )
