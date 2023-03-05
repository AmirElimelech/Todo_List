from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(allow_blank=True, required=False)
    complete = serializers.BooleanField(default=False)
    created = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return Task.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.complete = validated_data.get('complete', instance.complete)
        instance.save()
        return instance