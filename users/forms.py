from django.forms import ModelForm
from .models import Profile


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = [
            "name",
            "phone",
            "birthday",
            "location",
            "website",
            "bio",
            "profile_picture",
        ]
