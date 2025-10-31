from django import forms
from django.contrib.auth.forms import SetPasswordForm
from customer.models import Customer
from django.contrib.auth.hashers import make_password, check_password
import re
import hashlib
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password




# -----------------------
# Register Form
# -----------------------
class RegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(
        label=_("Confirm Password"),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password'
        }),
        required=True
    )

    email = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email address'
        }),
        required=True
    )

    class Meta:
        model = Customer
        fields = ['fullname', 'phone', 'username','address','email', 'password']
        widgets = {
            'fullname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Full name'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone number'
            }),
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Password'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Address'
            }),
        }

    # ----- VALIDATIONS -----
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if Customer.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if phone:
            if not re.match(r'^\+?\d{7,15}$', phone):
                raise forms.ValidationError("Phone number is not valid.")
            if Customer.objects.filter(phone=phone).exists():
                raise forms.ValidationError("Phone already exists.")
        return phone

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if username and Customer.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        if password:
            cleaned_data["password"] = make_password(password)

        return cleaned_data

# -----------------------
# Login Form
# -----------------------
class LoginForm(forms.Form):
    username = forms.CharField(
        label="Username",
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Username"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"})
    )
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input", "id": "rememberMe"})
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if not username or not password:
            raise forms.ValidationError("Please enter both username and password.")

        try:
            customer = Customer.objects.get(
                username=username, 
            )
        except Customer.DoesNotExist:
            raise forms.ValidationError("Invalid username or password.")
        
        if not check_password(password, customer.password):
            raise forms.ValidationError("Invalid username or password.")

        cleaned_data["customer"] = customer
        return cleaned_data



class UserPasswordResetForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your registered email address'
        }),
        label="Email"
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not Customer.objects.filter(email=email).exists():
            raise forms.ValidationError("No account found with this email.")
        return email
    
class UserSetPasswordForm(SetPasswordForm):
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

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()
