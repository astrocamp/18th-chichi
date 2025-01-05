from django.forms import ModelForm
from .models import Profile
import re
from django import forms
from django.utils.timezone import now


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
            "gender",
        ]
    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if phone:
            # 台灣手機號碼格式檢查
            if not re.match(r'^09\d{8}$', phone):
                raise forms.ValidationError("手機號碼必須是有效的台灣格式，如：09xxxxxxxx。")
        return phone
    
    def clean_birthday(self):
        birthday = self.cleaned_data.get("birthday")
        if birthday and birthday > now().date():
            raise forms.ValidationError("生日不能是未來的日期。")
        return birthday