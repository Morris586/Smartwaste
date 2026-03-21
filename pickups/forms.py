from django import forms
from .models import WastePickupRequest

class WastePickupForm(forms.ModelForm):
    class Meta:
        model= WastePickupRequest
        fields = ['name', 'address', 'phone', 'waste_type']
        