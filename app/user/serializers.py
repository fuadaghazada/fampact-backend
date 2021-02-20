from rest_framework import serializers

from .models import User


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
