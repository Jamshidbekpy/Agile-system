from rest_framework import serializers
from apps.task.models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("id", "title", "description","status", "priority", "rejection_comment")
        ref_name = "TaskDetailSerializer"

