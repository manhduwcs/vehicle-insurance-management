from django import forms
from .models import VehicleType, Vehicle, Claim

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
        fields = ["name", "customer", "model", "vehicle_type", "body_number", "engine_number", "number", "registration_date"]

class ClaimForm(forms.ModelForm):
    class Meta:
        model = Claim
        fields = ['vehicle', 'contract', 'place', 'date', 'human_damage', 'property_damage', 'deduction', 'personal_compensation', 'property_compensation', 'note']
        # fields = ["name", "fee", "description", "max_personal_compensation", "max_property_compensation"]

# class VehicleForm(forms.ModelForm):
#     class Meta:
#         model = Vehicle
#         fields = ["name", "customer", "model", "vehicle_type", "purchase_price", "body_number", "engine_number", "number", "registration_date"]
