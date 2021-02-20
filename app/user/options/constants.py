from django.utils.translation import gettext_lazy as _

USER_ROLE_ADMIN = 'ADMIN'
USER_ROLE_FAM_MEMBER = 'MEMBER'
USER_ROLE_PARENT = 'PARENT'
USER_ROLE_CHILD = 'CHILD'

USER_ROLE_CHOICES = (
    (USER_ROLE_FAM_MEMBER, _('Member')),
    (USER_ROLE_PARENT, _('Parent')),
    (USER_ROLE_CHILD, _('Child')),
)
