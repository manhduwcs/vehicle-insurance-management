from django import forms
from .models import InsuranceCategories, InsurancePriceList

class InsuranceCategoryForm(forms.ModelForm):
    class Meta:
        model = InsuranceCategories
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class InsurancePriceListForm(forms.ModelForm):
    class Meta:
        model = InsurancePriceList
        fields = ['rate']
        widgets = {
            'rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
        }