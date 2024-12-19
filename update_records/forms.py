from django.forms import ModelForm
from .models import UpdateRecord

class UpdateRecordFrom(ModelForm):
    class Meta:
        model = UpdateRecord
        fields = ["title", "description"]