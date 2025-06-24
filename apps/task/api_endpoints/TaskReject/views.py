from django.utils.translation import gettext_lazy as _
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.task.models import Task, TaskHistory
from apps.task.choices import TaskStatus
from apps.task.permissions import IsTester

class TaskRejectAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTester]


    def post(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response({"error": _("Task not found")}, status=404)

        reason = request.data.get("reason")
        if not reason:
            return Response({"error": _("Reason is required")}, status=400)

        task.status = TaskStatus.TO_DO
        task.rejection_comment = reason
        task.save()

        TaskHistory.objects.create(
            task=task,
            user=request.user,
            action=_("Status: Rejected (Reason: '{}')").format(reason)
        )

        return Response({"success": _("Task rejected and sent back to To Do")})

__all__ = ["TaskRejectAPIView"]