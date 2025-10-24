from django import forms
from .models import VehicleType, Vehicle

class VehicleTypeForm(forms.ModelForm):
    class Meta:
        model = VehicleType
        fields = [
            "name",
            "fee",
            "description",
            "max_personal_compensation",
            "max_property_compensation",
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'fee': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'max_personal_compensation': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'max_property_compensation': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ["name", "model", "vehicle_type", "purchase_price", "body_number", "engine_number", "number", "registration_date"]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'vehicle_type': forms.Select(attrs={'class': 'form-control'}),
            'purchase_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'body_number': forms.TextInput(attrs={'class': 'form-control'}),
            'engine_number': forms.TextInput(attrs={'class': 'form-control'}),
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'registration_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
