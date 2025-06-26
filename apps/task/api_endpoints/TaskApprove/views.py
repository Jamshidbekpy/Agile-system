from django.utils.translation import gettext_lazy as _
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.task.models import Task, TaskHistory
from apps.task.choices import TaskStatus
from apps.task.permissions import IsTester


class TaskApproveAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTester]

    def post(self, request, pk):
        user = request.user

        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response(
                {"error": _("Task not found")},
                status=status.HTTP_404_NOT_FOUND
            )

        if user not in task.assignees.all():
            return Response(
                {"error": _("You are not assigned to this task")},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if task.status != TaskStatus.READY_FOR_TESTING:
            return Response(
                {"error": _("Task is not ready for testing")},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        task.status = TaskStatus.DONE
        task.save()

        TaskHistory.objects.create(
            task=task,
            user=user,
            action=_("Status changed: Ready for Testing → Done")
        )

        return Response(
            {"success": _("Task approved and marked as Done")},
            status=status.HTTP_200_OK
        )



__all__ = ["TaskApproveAPIView"]