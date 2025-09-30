# employee/forms.py
from django import forms
from .models import Employees
from django.core.exceptions import ValidationError

class EmployeeForm(forms.ModelForm):
    re_password = forms.CharField(
        label='Re-enter Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = Employees
        fields = ['username', 'password', 're_password', 'fullname', 'email', 'phone', 'group']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'fullname': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'group': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].required = False
        self.fields['username'].required = True
        self.fields['email'].required = True
        self.fields['phone'].required = True
        self.fields['group'].required = True

    def clean_username(self):
        username = self.cleaned_data['username']
        queryset = Employees.objects.filter(username=username)
        if self.instance and self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise ValidationError("Username already exists. Please choose another username.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        queryset = Employees.objects.filter(email=email)
        if self.instance and self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise ValidationError("Email already exists. Please choose another email.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        queryset = Employees.objects.filter(phone=phone)
        if self.instance and self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise ValidationError("Phone number already exists. Please choose another phone number.")
        return phone


    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        re_password = cleaned_data.get('re_password')

        if password and re_password and password != re_password:
            raise ValidationError("Password and re-entered password do not match.")
        if not self.instance and not password:
            raise ValidationError("Password is required when creating new employee.")
        return cleaned_data

class LoginForm(forms.Form):
    login = forms.CharField(label='Username or Email', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))