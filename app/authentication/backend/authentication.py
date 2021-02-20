from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


User = get_user_model()


class EmailOrUsernameModelBackend(ModelBackend):
    """
        This model backend class utilized user email or username
        for authentication
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        """Authentication method"""
        if '@' in username:
            kw = 'email'
        else:
            kw = 'username'

        user_kwargs = {kw: username}
        try:
            user = User.objects.get(**user_kwargs)
            if user.check_password(raw_password=password):
                return user

        except User.DoesNotExist:
            return None

    def get_user(self, pk):
        """Getting the user via the Primary Key"""
        try:
            return User.objects.get(pk=pk)

        except User.DoesNotExist:
            return None
