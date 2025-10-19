from django import forms
from .models import Vehicles, Duration

class ContractForm(forms.Form):
    vehicle_id = forms.ModelChoiceField(
        queryset=Vehicles.objects.none(),
        empty_label="Select the vehicle you want to insure",
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'vehicle-select'}),
        required=True
    )
    duration_id = forms.ModelChoiceField(
        queryset=Duration.objects.all(),
        widget=forms.HiddenInput(),
        required=True
    )
    insurance_category_id = forms.IntegerField(
        widget=forms.HiddenInput(),
        required=True
    )

    def __init__(self, *args, **kwargs):
        customer_id = kwargs.pop('customer_id', None)
        super().__init__(*args, **kwargs)
        if customer_id:
            self.fields['vehicle_id'].queryset = Vehicles.objects.filter(CustomerID_id=customer_id)
