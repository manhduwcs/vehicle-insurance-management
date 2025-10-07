from django import forms
from .models import VehicleType, Vehicle

class VehicleTypeForm(forms.ModelForm):
    class Meta:
        model = VehicleType
        fields = ["name", "fee", "description", "max_claimable_amount"]

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ["name", "customer", "model", "vehicle_type", "rate", "body_number", "engine_number", "number", "registration_date"]
