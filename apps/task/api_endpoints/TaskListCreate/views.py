from django.utils.translation import gettext_lazy as _
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import TaskSerializer
from apps.task.models import Task, TaskHistory
from apps.task.permissions import IsProjectOwnerOrManager, IsAnyRole


class TaskListCreateAPIView(generics.ListCreateAPIView):
    queryset = Task.objects.all().select_related('assignee')
    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        task = serializer.save()
        TaskHistory.objects.create(
            task=task,
            user=self.request.user,
            action=_("Task created")
        )
    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), IsProjectOwnerOrManager()]
        return [IsAuthenticated(), IsAnyRole()]
        
__all__ = ["TaskListCreateAPIView"]