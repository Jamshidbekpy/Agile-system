from django.utils.translation import gettext_lazy as _
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.task.models import Task, TaskHistory
from apps.task.choices import TaskStatus
from apps.task.permissions import IsTester
class TaskApproveAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTester]


    def post(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response({"error": _("Task not found")}, status=404)

        task.status = TaskStatus.DONE
        task.save()

        TaskHistory.objects.create(
            task=task,
            user=request.user,
            action=_("Status changed: Ready for Testing → Done")
        )

        return Response({"success": _("Task approved and marked as Done")})


__all__ = ["TaskApproveAPIView"]