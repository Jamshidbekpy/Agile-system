from rest_framework import status
from django.utils.translation import gettext_lazy as _
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.task.models import Task, TaskHistory
from apps.task.choices import TaskStatus
from apps.task.permissions import IsTester
from .serializers import TaskRejectSerializer


class TaskRejectAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTester]

    def post(self, request, pk):
        user = request.user
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response({"error": _("Task not found")}, status=404)

        if user not in task.assignees.all():
            return Response(
                {"error": _("You are not assigned to this task")},
                status=status.HTTP_403_FORBIDDEN,
            )

        if task.status != TaskStatus.READY_FOR_TESTING:
            return Response(
                {"error": _("Task is not ready for testing")},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = TaskRejectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        reason = serializer.validated_data["reason"]
        if not reason:
            return Response({"error": _("Reason is required")}, status=400)
        
        
        task.status = TaskStatus.REJECTED
        task.rejection_comment = reason
        task.save()

        TaskHistory.objects.create(
            task=task,
            user=request.user,
            action=_("Status: Rejected (Reason: '{}')").format(reason),
        )

        return Response({"success": _("Task rejected and sent back to Rejected status")})


__all__ = ["TaskRejectAPIView"]
