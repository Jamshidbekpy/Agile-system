from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import TaskAssignSerializer
from apps.task.permissions import IsProjectOwner
from apps.task.models import Task

User = get_user_model()


class TaskAssignAPIView(APIView):
    permission_classes = [IsAuthenticated, IsProjectOwner]

    def post(self, request, pk):
        creator = request.user
        task = get_object_or_404(Task, pk=pk)
        if task.creator != creator:
            return Response(
                {"error": _("You are not the creator of this task")}, status=403
            )
        serializer = TaskAssignSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(task=task)
            return Response(
                {
                    "success": _(
                        f"User {serializer.validated_data['assignee']} was assigned to task {task.title}."
                    )
                }
            )
        return Response(serializer.errors, status=400)


__all__ = ["TaskAssignAPIView"]
