from rest_framework import serializers

from .models import Task
from user.serializers import BasicUserSerializer


class TaskInfoSerializer(serializers.ModelSerializer):
    """Task model info serializer"""
    created_by = BasicUserSerializer()
    assigned_to = BasicUserSerializer()

    class Meta:
        model = Task
        fields = (
            'id',
            'title',
            'status',
            'status_text',
            'deadline',
            'created_by',
            'assigned_to'
        )


class TaskDetailSerializer(TaskInfoSerializer):
    """Task model detail serializer"""

    class Meta:
        model = Task
        fields = TaskInfoSerializer.Meta.fields
        fields += (
            'description',
            'started_at',
            'finished_at',
        )


class TaskCreateUpdateSerializer(serializers.ModelSerializer):
    """Task model create/update serializer"""

    class Meta:
        model = Task
        fields = (
            'id',
            'title',
            'description',
            'assigned_to'
        )


class TaskStatusUpdateSerializer(serializers.ModelSerializer):
    """Task status update serializer"""

    class Meta:
        model = Task
        fields = (
            'status'
        )

    def update(self, instance, validated_data):
        """Adding request user to """
        user = self.context.get('user')

        instance.user = user
        instance.status = validated_data.get('status')
        instance.save()

        return instance
