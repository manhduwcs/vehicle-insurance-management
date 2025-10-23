from django import forms
from .models import VehicleTypes

class VehicleTypeForm(forms.ModelForm):
    class Meta:
        model = VehicleTypes
        fields = ['name', 'fee', 'description', 'max_personal_compensation', 'max_property_compensation']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'fee': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'max_personal_compensation': forms.NumberInput(attrs={'class': 'form-control'}),
            'max_property_compensation': forms.NumberInput(attrs={'class': 'form-control'}),
        }