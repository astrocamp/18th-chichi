from django.forms import ModelForm
from .models import Pledges


class PledgesForm(ModelForm):
    class Meta:
        model = Pledges
        fields = [
            "pledges_amount",
            "payment_status",
        ]
