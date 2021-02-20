from app.celery import app
from core.utils.email import send_email as send_mail


@app.task
def send_email(subject, emails: list, content):
    """Sending verification email to the user"""
    send_mail(subject, emails, content)

    return f"Email sent to: {emails}"
