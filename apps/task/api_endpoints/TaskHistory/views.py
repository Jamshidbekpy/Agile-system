from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.task.models import TaskHistory
from apps.task.permissions import IsAnyRole
from .serializers import TaskHistorySerializer


class TaskHistoryAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAnyRole]

    def get(self, request, pk):
        histories = (
            TaskHistory.objects.filter(task_id=pk)
            .select_related("user")
            .order_by("timestamp")
        )
        serializer = TaskHistorySerializer(histories, many=True)
        return Response({"task_id": pk, "history": serializer.data})


__all__ = ["TaskHistoryAPIView"]
