from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Task, TaskStatusLog


@receiver(post_save, sender=Task)
def task_status_updated(sender, **kwargs):
    """
    Creating log for every task status updated

    :param sender:
    :param kwargs:
    :return:
    """
    task = kwargs.get('instance')
    user = task.user if hasattr(task, 'user') else None

    if task._status == task.status:
        return

    TaskStatusLog.objects.create(
        task=task,
        status=task.status,
        user=user
    )
