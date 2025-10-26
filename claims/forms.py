from django import forms
from .models import Claim
from vehicles.models import Vehicles
from contracts.models import Contracts

class ClaimForm(forms.ModelForm):
    class Meta:
        model = Claim
        fields = [
         'contract', 'place', 'date',
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }



class ClaimApprovalForm(forms.ModelForm):
    """
    Form for employees to update compensation details when approving a claim
    """
    
    class Meta:
        model = Claim
        fields = [
            'human_damage',
            'property_damage',
            'deduction',
            'personal_compensation',
            'property_compensation',
            'note',
        ]
        widgets = {
            'human_damage': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter human damage amount',
                'step': '0.01',
            }),
            'property_damage': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter property damage amount',
                'step': '0.01',
            }),
            'deduction': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter deduction amount',
                'step': '0.01',
            }),
            'personal_compensation': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter personal compensation amount',
                'step': '0.01',
            }),
            'property_compensation': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter property compensation amount',
                'step': '0.01',
            }),
            'note': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Additional notes about this claim...',
            }),
        }
        labels = {
            'human_damage': 'Human Damage (VND)',
            'property_damage': 'Property Damage (VND)',
            'deduction': 'Deduction (VND)',
            'personal_compensation': 'Personal Compensation (VND)',
            'property_compensation': 'Property Compensation (VND)',
            'note': 'Notes',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make all fields required for approval
        for field_name in self.fields:
            if field_name != 'note':  # Note is optional
                self.fields[field_name].required = True