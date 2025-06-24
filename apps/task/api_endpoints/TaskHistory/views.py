from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import TaskHistorySerializer
from apps.task.models import TaskHistory
from apps.task.permissions import IsAnyRole
class TaskHistoryAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsAnyRole]
    serializer_class = TaskHistorySerializer


    def get_queryset(self):
        task_id = self.kwargs.get("pk")
        return TaskHistory.objects.filter(task_id=task_id).select_related("user")
    
__all__ = ["TaskHistoryAPIView"]