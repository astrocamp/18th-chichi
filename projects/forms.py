from django.forms import ModelForm, ModelMultipleChoiceField, CheckboxSelectMultiple
from .models import Project, Category


class ProjectFrom(ModelForm):
    categories = ModelMultipleChoiceField(
        queryset=Category.objects.all(), widget=CheckboxSelectMultiple
    )

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
            "cover_image",
            "categories",
        ]
