from rest_framework import serializers
from .models import ProjectCalendar


class ProjectCalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectCalendar
        fields = ["id", "title", "start_at", "end_at"]

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "title": instance.title,
            "start": instance.start_at.isoformat() if instance.start_at else None,
            "end": instance.end_at.isoformat() if instance.end_at else None,
        }
