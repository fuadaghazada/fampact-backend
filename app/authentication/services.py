from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token

from core.tasks import send_email
from core.utils import cache, helpers, timezone

# Redis keys
VERIFICATION_KEY = 'VERIFICATION_KEY'
RESET_PASSWORD_TOKEN_KEY = 'RESET_PASSWORD_TOKEN_KEY'


def login(request, username, password):
    """Login service (non-merchant & merchant users): returns the token"""
    user = authenticate(
        request=request,
        username=username,
        password=password
    )

    if not user:
        raise Exception(_('Email or password is wrong'))
    if not user.verified_at:
        raise Exception(_('Please verify the user'))

    token = get_auth_token(user)

    return token


def send_verification(user):
    """Send verification to the given user"""
    verification_code = helpers.random_code()
    cache.set_key(
        pre_key=VERIFICATION_KEY,
        key=user.pk,
        value=verification_code
    )

    send_email.delay(_('Verification code'), [user.email], verification_code)

    return user


def verify_user(user, verification_code):
    """Verifies the user given the verification code entered"""
    actual_verification_code = cache.get_key(
        pre_key=VERIFICATION_KEY,
        key=user.pk
    )
    if not actual_verification_code:
        raise Exception(_('Verification code has been expired'))

    if actual_verification_code != verification_code:
        raise Exception(_('The verification code you entered is incorrect'))

    cache.remove_key(pre_key=VERIFICATION_KEY, key=user.pk)

    # Generating a token for 'set_password'
    if not user.verified_at:
        user.verified_at = timezone.now()
        user.save()

    set_password_token = str(helpers.random_code(20)).lower()
    cache.set_key(
        pre_key=RESET_PASSWORD_TOKEN_KEY,
        key=set_password_token,
        value=user.id
    )

    return user, set_password_token


def set_password(user, password, token):
    """Setting the password"""
    if not token:
        raise Exception(_('Token is required'))

    user_id = cache.get_key(pre_key=RESET_PASSWORD_TOKEN_KEY, key=token)

    if not user_id or int(user_id) != user.id:
        raise Exception(_('Invalid token'))

    user.set_password(password)
    user.save()

    cache.remove_key(pre_key=RESET_PASSWORD_TOKEN_KEY, key=token)

    return user


def logout(user):
    """Logout service"""
    try:
        token, _ = Token.objects.get_or_create(user=user)
        token.delete()

    except Token.DoesNotExist:
        pass


def get_auth_token(user):
    """Getting the token for auth"""
    token, __ = Token.objects.get_or_create(user=user)

    return str(token)
