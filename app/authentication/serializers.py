from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from .validators import PASSWORD_VALIDATOR

User = get_user_model()


class LoginUserSerializer(serializers.Serializer):
    """Serializer for user authentication"""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )


class ForgotPasswordSerializer(serializers.Serializer):
    """Serializer for forgot password field validation"""
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get('email')

        try:
            user = User.objects.get(email=email)
            attrs['user'] = user

        except User.DoesNotExist:
            raise serializers.ValidationError({
                'email': _('No user found with this email')
            })

        return attrs


class VerifyUserSerializer(serializers.Serializer):
    """Serializer for verifying the user"""
    verification_code = serializers.CharField()


class SetPasswordSerializer(serializers.Serializer):
    """Serializer for setting password"""
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
        validators=PASSWORD_VALIDATOR
    )


class BasicUserSerializer(serializers.ModelSerializer):
    """Serializer for basic user fields"""

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'verified_at'
        )
        extra_kwargs = {
            'verified_at': {'read_only': True}
        }


class RegisterUserSerializer(serializers.ModelSerializer):
    """Register user serializer"""
    name = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
        validators=PASSWORD_VALIDATOR
    )

    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'password')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def validate(self, attrs):
        name = attrs.pop('name')
        parts = str(name).strip().split(" ")
        if len(parts) != 2:
            raise serializers.ValidationError({
                'name': _('Please enter name and surname')
            })

        attrs['first_name'] = parts[0]
        attrs['last_name'] = parts[1]

        return attrs
