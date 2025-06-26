from rest_framework import serializers
from apps.task.models import Task
from apps.task.choices import TaskPriority


class TaskChangePrioritySerializer(serializers.ModelSerializer):
    priority = serializers.ChoiceField(choices=TaskPriority.CHOICES)

    class Meta:
        model = Task
        fields = ("priority",)
