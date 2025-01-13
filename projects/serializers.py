from rest_framework import serializers
from .models import Project, ProjectCalendar


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "title", "slug"]


class ProjectCalendarSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)

    class Meta:
        model = ProjectCalendar
        fields = ["id", "title", "start_at", "end_at", "project"]

    def to_representation(self, instance):

        return {
            "id": instance.id,
            "title": instance.title,
            "start": instance.start_at.isoformat() if instance.start_at else None,
            "end": instance.end_at.isoformat() if instance.end_at else None,
        }
