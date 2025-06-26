from rest_framework import serializers
from apps.task.models import Task
from django.contrib.auth import get_user_model

User = get_user_model()
class UserSerilalizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "role")

class TaskSerializer(serializers.ModelSerializer):
    assigned_to = UserSerilalizer(source="assignees", many=True, read_only=True)
    class Meta:
        model = Task
        fields = ("id", "creator", "title", "description", "assigned_to", "status", "priority", "rejection_comment")
        extra_kwargs = {
            "status": {"read_only": True},
            "creator": {"read_only": True},
        }
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.creator:
            data["creator"] = UserSerilalizer(instance.creator).data.get("username", None)
        else:
            data["creator"] = None
        return data

