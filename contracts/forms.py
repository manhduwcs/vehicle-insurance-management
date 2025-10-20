from django import forms
from vehicle.models import Vehicle
from categories.models import Duration
from .models import ContractStatus, Contracts

class ContractForm(forms.Form):
    vehicle_id = forms.ModelChoiceField(
        queryset=Vehicle.objects.none(),
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
            # self.fields['vehicle_id'].queryset = Vehicle.objects.filter(customer_id=customer_id)
            queryset = Vehicle.objects.filter(customer_id=customer_id)
            self.fields['vehicle_id'].queryset = queryset
            self.fields['vehicle_id'].label_from_instance = lambda obj: f"{obj.name} - {obj.number}"

# for update contract only
class ContractUpdateForm(forms.ModelForm):
    class Meta:
        model = Contracts
        fields = [
            'deductible_value',
            'deductible_addon',
            'actual_value',
            'actual_premium',
            'status',
            'note',
        ]
        widgets = {
            'deductible_value': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'deductible_addon': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'actual_value': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'actual_premium': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'status': forms.Select(attrs={
                'class': 'form-select',  # applies Bootstrap/Soft UI style
            }),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


    def __init__(self, *args, **kwargs):
        contract = kwargs.pop('instance', None)
        super().__init__(*args, **kwargs)

        if contract:
            allowed = ContractStatus.transitions().get(contract.status, [])
            self.fields["status"].choices = [
                (s.value, s.label)
                for s in allowed
            ]
            print(f"current contract status: {contract.status}")
            self.fields['status'].initial = contract.status


    def clean(self):
        cleaned_data = super().clean()
        deductible_value = cleaned_data.get('deductible_value')
        deductible_addon = cleaned_data.get('deductible_addon')
        actual_value = cleaned_data.get('actual_value')
        actual_premium = cleaned_data.get('actual_premium')

        # ✅ Validate numeric fields
        for field in ['deductible_value', 'deductible_addon', 'actual_value', 'actual_premium']:
            value = cleaned_data.get(field)
            if value is not None and value < 0:
                self.add_error(field, "Value must be non-negative.")

        # ✅ Logical consistency checks
        if actual_premium and isinstance(actual_premium, (int, float)) and actual_premium > actual_value:
            self.add_error('actual_premium', "Actual premium cannot exceed actual value.")

        return cleaned_data
