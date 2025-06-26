from rest_framework import serializers
from apps.task.models import Task
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerilalizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "role", "email")

class TaskSerializer(serializers.ModelSerializer):
    assigned_to = UserSerilalizer(source="assignees", many=True, read_only=True)
    class Meta:
        model = Task
        fields = ("id", "creator", "title", "assigned_to", "description","status", "priority", "rejection_comment")
        ref_name = "TaskDetailSerializer"
        
        extra_kwargs = {
            "status": {"read_only": True},
            "creator": {"read_only": True},
        }

