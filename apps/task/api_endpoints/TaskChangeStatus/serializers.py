from rest_framework import serializers

class TaskChangeStatusSerializer(serializers.Serializer):
    status = serializers.CharField()