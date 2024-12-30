from django import forms
from .models import Reward , RewardProduct, OptionalAdd

class RewardForm(forms.ModelForm):
    class Meta:
        model = Reward
        fields = [
            "title", 
            "description",
            "quantity",
            "price", 
            "estimated_delivery", 
        ]

class ProductForm(forms.ModelForm):
    class Meta:
        model = RewardProduct
        fields = ['name']

class AddOnForm(forms.ModelForm):
    class Meta:
        model = OptionalAdd
        fields = ['name', 'price']