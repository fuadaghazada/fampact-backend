from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Task
from .serializers import (
    TaskInfoSerializer,
    TaskDetailSerializer,
    TaskCreateUpdateSerializer,
    TaskStatusUpdateSerializer
)


class TaskViewSet(viewsets.ModelViewSet):
    """Task model view set"""
    queryset = Task.objects.all().order_by('-created_at')

    @action(detail=True, methods=['PUT'])
    def update_status(self, request, pk):
        context = self.get_serializer_context()
        context.update({'user': request.user})
        serializer = self.get_serializer_class()(
            data=request,
            context=context
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            TaskDetailSerializer(serializer.instance).data
        )

    def get_queryset(self):
        return Task.objects.all()

    def get_serializer_class(self):
        """
        * List -> task info
        * Retrieve -> task detail
        * Create/Update -> task create & update
        * Delete

        :return:
        """
        if self.action in ['list']:
            return TaskInfoSerializer
        elif self.action in ['retrieve']:
            return TaskDetailSerializer
        elif self.action in ['create', 'update']:
            return TaskCreateUpdateSerializer
        elif self.action in ['update_status']:
            return TaskStatusUpdateSerializer

        return TaskInfoSerializer
