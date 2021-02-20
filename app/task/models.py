from django.db import models
from django.utils.translation import gettext_lazy as _

from core.abstract_models import TimestampMixin
from task.options.constants import (
    TASK_STATUS_CHOICES,
    TASK_STATUS_PENDING
)


class Task(TimestampMixin):
    """Task model"""
    title = models.CharField(
        _('Title'),
        max_length=255
    )
    description = models.TextField(
        _('Description'),
        null=True,
        blank=True
    )
    status = models.CharField(
        _('Status'),
        max_length=255,
        choices=TASK_STATUS_CHOICES,
        default=TASK_STATUS_PENDING
    )
    deadline = models.DateTimeField(
        _('Deadline'),
        null=True,
        blank=True
    )
    started_at = models.DateTimeField(
        _('Started at'),
        null=True,
        blank=True
    )
    finished_at = models.DateTimeField(
        _('Finished at'),
        null=True,
        blank=True
    )
    created_by = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        related_name='user_created_tasks',
        verbose_name=_('Task creator')
    )
    assigned_to = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        related_name='user_assigned_tasks',
        verbose_name=_('Task assignee'),
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')

    def __init__(self, *args, **kwargs):
        super(Task, self).__init__(*args, **kwargs)
        self._status = self.status

    @property
    def status_text(self):
        return self.get_status_display()

    def __str__(self):
        return self.title


class TaskStatusLog(TimestampMixin):
    """Task log model"""
    status = models.CharField(
        _('Status'),
        max_length=255
    )
    task = models.ForeignKey(
        'Task',
        on_delete=models.CASCADE,
        related_name='task_logs'
    )
    updated_by = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        related_name='user_task_logs',
        verbose_name=_('Task log updater'),
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = _('Task log')
        verbose_name_plural = _('Task logs')

    def __str__(self):
        return f"Task #{self.pk}: {self.status}"
