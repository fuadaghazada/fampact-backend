from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import (
    CreateAPIView,
    UpdateAPIView
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from authentication.serializers import (
    LoginUserSerializer,
    ForgotPasswordSerializer,
    VerifyUserSerializer,
    SetPasswordSerializer,
    RegisterUserSerializer
)
from user.serializers import BasicUserSerializer
from authentication.services import (
    login,
    verify_user,
    send_verification,
    set_password,
    logout,
    get_auth_token
)

User = get_user_model()


class LoginAPIView(CreateAPIView):
    """Login API view"""
    serializer_class = LoginUserSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            token = login(**data, request=request)
            return Response({'token': str(token)})

        except Exception as e:
            return Response(
                {'error': True, 'message': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class ForgotAPIView(CreateAPIView):
    """Forgot API view"""
    serializer_class = ForgotPasswordSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        user = data.get('user')
        send_verification(user=data.get('user'))

        return Response(BasicUserSerializer(user).data)


class VerifyAPIView(UpdateAPIView):
    """Verify API view"""
    queryset = User.objects.exclude(is_superuser=True)
    serializer_class = VerifyUserSerializer
    permission_classes = (AllowAny,)

    def put(self, request, *args, **kwargs):
        user = self.get_object()

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            user, token = verify_user(user, **data)
            response_data = BasicUserSerializer(user).data
            if token:
                response_data['reset_password_token'] = token
            return Response(response_data)

        except Exception as e:
            return Response(
                {'error': True, 'message': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class SetPasswordAPIView(UpdateAPIView):
    """Set password API view"""
    queryset = User.objects.exclude(is_superuser=True)
    serializer_class = SetPasswordSerializer
    permission_classes = (AllowAny,)

    def put(self, request, *args, **kwargs):
        user = self.get_object()

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        token = kwargs.get('token')

        try:
            user = set_password(user=user, token=token, **data)
            return Response(BasicUserSerializer(user).data)

        except Exception as e:
            return Response(
                {'error': True, 'message': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class LogoutAPIView(APIView):
    """Logout API View"""

    def post(self, request, *args, **kwargs):
        logout(request.user)
        return Response({'message': _('Logout successful')})


class RegisterAPIView(CreateAPIView):
    """Register API View"""
    serializer_class = RegisterUserSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response_data = BasicUserSerializer(serializer.instance).data
        token = get_auth_token(serializer.instance)
        response_data.update({'token': token})

        return Response(response_data)
