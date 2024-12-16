from django import forms
from .models import Reward

class RewardForm(forms.ModelForm):
    class Meta:
        model = Reward
        fields = [
            "title", 
            "description",
            "quantity",
            "price", 
            "pledge_amount", 
            "ship_to", 
            "shipping_detail", 
            "estimated_delivery", 
            "optional_adds_on",
        ]
