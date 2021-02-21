from rest_framework.permissions import BasePermission

from user.options.constants import USER_ROLE_PARENT


class IsParent(BasePermission):
    """
    Parent
    """

    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            not request.user.role == USER_ROLE_PARENT
        )
