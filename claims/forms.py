from django import forms
from .models import Claim
from vehicle.models import Vehicle
from contracts.models import Contracts

class ClaimForm(forms.ModelForm):
    class Meta:
        model = Claim
        fields = [
            'vehicle', 'contract', 'place', 'date',
            'human_damage', 'property_damage', 'deduction',
            'personal_compensation', 'property_compensation', 'note'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }