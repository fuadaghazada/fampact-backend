from django.db import models
from django.utils.translation import gettext_lazy as _

from core.abstract_models import TimestampMixin


class Score(TimestampMixin):
    """Score model"""
    score = models.PositiveIntegerField()
    user = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        related_name='user_scores',
        verbose_name=_('Score of user')
    )
    task = models.ForeignKey(
        'task.Task',
        on_delete=models.CASCADE,
        related_name='task_scores',
        verbose_name=_('Score for task'),
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _('Score')
        verbose_name_plural = _('Scores')
