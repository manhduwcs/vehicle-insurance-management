from django import forms
from .models import Vehicles, VehicleTypes

class VehicleForm(forms.ModelForm):
    vehicle_type = forms.ModelChoiceField(queryset=VehicleTypes.objects.all(), empty_label="Select Vehicle Type")

    class Meta:
        model = Vehicles
        fields = ['name', 'model', 'vehicle_type', 'purchase_price', 'body_number', 'engine_number', 'number', 'registration_date']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'purchase_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'body_number': forms.TextInput(attrs={'class': 'form-control'}),
            'engine_number': forms.TextInput(attrs={'class': 'form-control'}),
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'registration_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }