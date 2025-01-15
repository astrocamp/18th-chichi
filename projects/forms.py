from django.forms import (
    ModelForm,
    Form,
    ModelMultipleChoiceField,
    CheckboxSelectMultiple,
    CharField,
    TextInput,
    ChoiceField,
    Select,
)
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


class ProjectSearchForm(Form):
    query = CharField(
        max_length=255,
        required=False,
        widget=TextInput(
            attrs={"placeholder": "搜尋標題或描述...", "class": "form-control"}
        ),
    )
    status = ChoiceField(
        choices=[("", "全部狀態")] + Project.STATUS_CHOICES,
        required=False,
        widget=Select(attrs={"class": "form-select"}),
    )
    location = CharField(
        max_length=100,
        required=False,
        widget=TextInput(attrs={"placeholder": "地點", "class": "form-control"}),
    )
    categories = ModelMultipleChoiceField(
        queryset=Category.objects.all(), required=False, label="分類"
    )
