from django import forms
from .models import InsuranceCategory

class InsuranceCategoryForm(forms.ModelForm):
    class Meta:
        model = InsuranceCategory
        fields = ["name", "fee", "rate", "type", "description"]