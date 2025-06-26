from rest_framework import serializers
from apps.task.models import TaskHistory


class TaskHistorySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = TaskHistory
        fields = ("user", "action", "timestamp")
