from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "Enter a valid email"})
    )

    class Meta:
        model = Customer
        fields = ['fullname', 'address', 'email', 'phone', 'username']

    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = Customer.objects.filter(email=email).exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Email already exists.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        qs = Customer.objects.filter(phone=phone).exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Phone number already exists.")
        return phone

    def clean_username(self):
        username = self.cleaned_data.get("username")
        qs = Customer.objects.filter(username=username).exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Username already exists.")
        return username


class CustomerUpdateForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['fullname', 'email', 'phone', 'address','identify_number','identify_address','identify_date','issuing_authority','tax_id']

    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = Customer.objects.filter(email=email).exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Email already exists.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        qs = Customer.objects.filter(phone=phone).exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Phone number already exists.")
        return phone
