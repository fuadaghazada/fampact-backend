from rest_framework import serializers

from .models import User, Family


class BasicUserSerializer(serializers.ModelSerializer):
    """Serializer for basic user fields"""

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
            'role',
            'role_text'
        )
        extra_kwargs = {
            'verified_at': {'read_only': True}
        }


class FamilySerializer(serializers.ModelSerializer):
    """Family model serializer"""
    members = BasicUserSerializer(source='family_members', many=True)

    class Meta:
        model = Family
        fields = (
            'id',
            'name',
            'members'
        )


class AddFamilyMemberSerializer(serializers.ModelSerializer):
    """Add member to family"""
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'email',
        )

    def create(self, validated_data):
        return User.objects.add_member(**validated_data)

    def validate(self, attrs):
        attrs['adder'] = self.context.get('request').user

        return attrs


class AddChildMemberSerializer(serializers.ModelSerializer):
    """Add Child to family"""

    class Meta:
        model = User
        fields = (
            'first_name',
            'username',
            'password'
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        return User.objects.add_child(**validated_data)

    def validate(self, attrs):
        attrs['adder'] = self.context.get('request').user

        return attrs
