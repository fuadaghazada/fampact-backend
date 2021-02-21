from rest_framework import serializers

from user.models import User, Family
from user.serializers import BasicUserSerializer


class PublicLeaderBoardSerializer(serializers.ModelSerializer):
    """Public leader board serializer"""
    score = serializers.IntegerField(default=0)

    class Meta:
        model = Family
        fields = (
            'id',
            'name',
            'photo',
            'region',
            'score'
        )


class FamilyMemberLeaderBoardSerializer(BasicUserSerializer):
    """Family member leader board serializer"""
    score = serializers.IntegerField(default=0)

    class Meta:
        model = User
        fields = BasicUserSerializer.Meta.fields
        fields += (
            'score',
        )
