from rest_framework import serializers
from apps.task.models import TaskAssignee


class TaskAssignSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskAssignee
        fields = (
            "id",
            "task",
            "assignee",
        )
        read_only_fields = ("task",)
