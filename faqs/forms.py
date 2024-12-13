from django.forms import ModelForm
from .models import Faq

class FaqForm(ModelForm):
     class Meta:
          model = Faq
          fields = ["project", "question", "answer"]