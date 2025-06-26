from rest_framework import serializers


class TaskRejectSerializer(serializers.Serializer):
    reason = serializers.CharField()
