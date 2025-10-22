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

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ["name", "customer", "model", "vehicle_type", "purchase_price", "body_number", "engine_number", "number", "registration_date"]
