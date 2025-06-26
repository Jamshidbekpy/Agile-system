from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import TaskSerializer
from apps.task.models import Task
from apps.task.permissions import IsProjectOwner, IsAnyRole



class TaskRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all().prefetch_related('assignees')
    serializer_class = TaskSerializer
    
    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [IsAuthenticated(), IsProjectOwner()]
        return [IsAuthenticated(), IsAnyRole()]

    
__all__ = ['TaskRetrieveUpdateDestroyAPIView']