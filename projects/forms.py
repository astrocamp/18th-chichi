from django.forms import ModelForm, CheckboxSelectMultiple
from .models import Project


class ProjectFrom(ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "subtitle",
            "start_at",
            "end_at",
            "goal_amount",
            "story",
            "location",
            "category",
            "subcategories",
        ]
        widgets = {
            "subcategories": CheckboxSelectMultiple,
        }
