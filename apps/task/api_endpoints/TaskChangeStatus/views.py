from django.utils.translation import gettext_lazy as _
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.task.choices import TaskStatus
from apps.task.models import Task, TaskHistory
from .serializers import TaskChangeStatusSerializer
from apps.task.permissions import IsProjectManager, IsDeveloper



class TaskChangeStatusAPIView(APIView):
    permission_classes = [IsAuthenticated, IsProjectManager | IsDeveloper]


    def post(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response({"error": _("Task not found")}, status=404)
        
        if task.status in [TaskStatus.BACKLOG, TaskStatus.REJECTED, TaskStatus.DONE] and request.user.role == "developer":
            return Response({"error": _("You can't change the status of this task")}, status=403)
        
        if task.status in [TaskStatus.IN_PROGRESS, TaskStatus.READY_FOR_TESTING,TaskStatus.REJECTED, TaskStatus.DONE] and request.user.role == "project_manager":
            return Response({"error": _("You can't change the status of this task")}, status=403)
        
        serializer = TaskChangeStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        new_status = serializer.validated_data["status"]
        
        if new_status in [TaskStatus.BACKLOG, TaskStatus,TaskStatus.REJECTED, TaskStatus.DONE] and request.user.role == "developer":
            return Response({"error": _("You can't change the status of this task")}, status=403)
        
        if new_status in [TaskStatus.IN_PROGRESS, TaskStatus.READY_FOR_TESTING,TaskStatus.REJECTED, TaskStatus.DONE] and request.user.role == "project_manager":
            return Response({"error": _("You can't change the status of this task")}, status=403)    
            
        if new_status not in dict(TaskStatus.CHOICES):
            return Response({"error": _("Invalid status")}, status=400)

        old_status = task.status
        task.status = new_status
        task.save()

        TaskHistory.objects.create(
            task=task,
            user=request.user,
            action=_("Status changed: {} → {}").format(old_status, new_status)
        )

        return Response({"success": _("Status updated")})
    
__all__ = ["TaskChangeStatusAPIView"]