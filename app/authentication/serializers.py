from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from .validators import PASSWORD_VALIDATOR

User = get_user_model()


class LoginUserSerializer(serializers.Serializer):
    """Serializer for user authentication"""
    username = serializers.CharField()
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


class RegisterUserSerializer(serializers.ModelSerializer):
    """Register user serializer"""
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
        validators=PASSWORD_VALIDATOR
    )

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'password'
        )

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class TokenUserSerializer(serializers.ModelSerializer):
    """Serializer for basic user fields"""
    family = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'full_name',
            'email',
            'username',
            'verified_at',
            'family',
            'role',
            'role_text'
        )
        extra_kwargs = {
            'verified_at': {'read_only': True}
        }

    def get_family(self, obj):
        if not obj.family:
            return

        return {
            'id': obj.family.id,
            'name': obj.family.name
        }
