from django import forms
from .models import Discount

class DiscountForm(forms.ModelForm):
    class Meta:
        model = Discount
        fields = ['name', 'rate', 'description']