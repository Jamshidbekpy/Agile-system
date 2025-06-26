from django.urls import path
from .api_endpoints import (
    TaskListCreateAPIView,
    TaskRetrieveUpdateDestroyAPIView,
    TaskChangeStatusAPIView,
    TaskRejectAPIView,
    TaskApproveAPIView,
    TaskHistoryAPIView,
    TaskAssignAPIView,
    TaskChangePriorityAPIView,
)

urlpatterns = [
    path("", TaskListCreateAPIView.as_view(), name="task-list-create"),
    path("<int:pk>/", TaskRetrieveUpdateDestroyAPIView.as_view(), name="task-detail"),
    path(
        "<int:pk>/change_status/",
        TaskChangeStatusAPIView.as_view(),
        name="task-change-status",
    ),
    path("<int:pk>/reject/", TaskRejectAPIView.as_view(), name="task-reject"),
    path("<int:pk>/approve/", TaskApproveAPIView.as_view(), name="task-approve"),
    path("<int:pk>/assign/", TaskAssignAPIView.as_view(), name="task-assign"),
    path(
        "<int:pk>/change_priority/",
        TaskChangePriorityAPIView.as_view(),
        name="task-change-priority",
    ),
    path("<int:pk>/history/", TaskHistoryAPIView.as_view(), name="task-history"),
]
