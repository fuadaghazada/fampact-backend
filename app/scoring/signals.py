from django.db.models.signals import post_save
from django.dispatch import receiver

from task.models import Task
from task.options.constants import (
    TASK_STATUS_PENDING,
    TASK_STATUS_DOING,
    TASK_STATUS_DONE
)
from .models import Score


@receiver(post_save, sender=Task)
def handle_score(sender, **kwargs):
    """
    Handling score acc. to Task status

    :param sender:
    :param kwargs:
    :return:
    """
    task = kwargs.get('instance')
    user = task.user if hasattr(task, 'user') else None

    if task.status in [TASK_STATUS_PENDING, TASK_STATUS_DOING]:
        Score.objects.filter(task=task).delete()

    if task.status == TASK_STATUS_DONE:
        Score.objects.get_create(
            score=1,
            user=user,
            task=task
        )
