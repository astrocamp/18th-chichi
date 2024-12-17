from django.forms import ModelForm
from .models import User


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = [
            "name",
            "phone",
            "birthday",
            "location",
            "website",
            "bio",
            "profile_picture",
        ]
