# employee/forms.py
from django import forms
from django.contrib.auth.forms import SetPasswordForm

from .models import Employees
from django.core.exceptions import ValidationError
from accounts.forms import hash_password
from django.db.models import Q

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

    def clean(self):
        cleaned_data = super().clean()
        login_input = cleaned_data.get("login")
        password = cleaned_data.get("password")

        if not login_input or not password:
            raise ValidationError("Please enter both username/email and password.")

        hashed_password = hash_password(password)
        try:
            employee = Employees.objects.filter(
                (Q(username=login_input) | Q(email=login_input)) & Q(password=hashed_password)
            ).first()
            if not employee:
                raise ValidationError("Invalid username/email or password.")
            cleaned_data["employee"] = employee
        except Exception as e:
            raise ValidationError("Invalid username/email or password.")

        return cleaned_data

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        label='Old Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True
    )
    new_password = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True
    )
    re_type_password = forms.CharField(
        label='Re-type New Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True
    )

    def __init__(self, employee, *args, **kwargs):
        self.employee = employee
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get('old_password')
        new_password = cleaned_data.get('new_password')
        re_type_password = cleaned_data.get('re_type_password')

        if not old_password or not new_password or not re_type_password:
            raise ValidationError("All fields are required.")

        # Check old password
        if old_password and hash_password(old_password) != self.employee.password:
            raise ValidationError("Incorrect old password.")

        # Check new password match
        if new_password != re_type_password:
            raise ValidationError("New password and re-typed password do not match.")

        # Hash new password
        cleaned_data['new_password'] = hash_password(new_password)
        return cleaned_data

class EmployeeUpdateForm(forms.ModelForm):
    class Meta:
        model = Employees
        fields = ['fullname', 'email', 'phone']

    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = Employees.objects.filter(email=email).exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Email already exists.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        qs = Employees.objects.filter(phone=phone).exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Phone number already exists.")
        return phone


class EmployeePasswordResetForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address'
        }),
        label="Email"
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not Employees.objects.filter(email=email).exists():
            raise forms.ValidationError("No account found with this email.")
        return email


class EmployeeSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'New Password'
        }),
        label="New Password"
    )
    new_password2 = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm New Password'
        }),
        label="Confirm New Password"
    )
