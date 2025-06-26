from django.utils.translation import gettext_lazy as _
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.task.models import Task, TaskHistory
from .serializers import TaskChangePrioritySerializer
from apps.task.permissions import IsProjectManager


class TaskChangePriorityAPIView(APIView):
    permission_classes = [IsAuthenticated, IsProjectManager]

    def post(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response(
                {"error": _("Task not found")}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = TaskChangePrioritySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_priority = serializer.validated_data["priority"]

        old_priority = task.priority
        task.priority = new_priority
        task.save()

        TaskHistory.objects.create(
            task=task,
            user=request.user,
            action=_("Priority changed: {} → {}").format(old_priority, new_priority),
        )

        return Response(
            {"success": _("Task priority updated")}, status=status.HTTP_200_OK
        )


__all__ = [
    "TaskChangePriorityAPIView",
]
