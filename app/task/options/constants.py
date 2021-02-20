from django.utils.translation import gettext_lazy as _

TASK_STATUS_PENDING = 'PENDING'
TASK_STATUS_DOING = 'DOING'
TASK_STATUS_DONE = 'DONE'

TASK_STATUS_CHOICES = (
    (TASK_STATUS_PENDING, _('Pending')),
    (TASK_STATUS_DOING, _('DOING')),
    (TASK_STATUS_DONE, _('DONE')),
)
