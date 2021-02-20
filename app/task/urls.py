from django.urls import path, include
from rest_framework import routers

from .views import (
    TaskViewSet,
)

app_name = 'task'

router = routers.DefaultRouter()
router.register('', TaskViewSet, basename='tasks')

urlpatterns = [
    path('tasks/', include(router.urls), name="tasks")
]
