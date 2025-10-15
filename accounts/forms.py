from django import forms
from customer.models import Customer
import hashlib
import re
# Hàm hash password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# -----------------------
# Register Form
# -----------------------
class RegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = Customer
        fields = ['fullname', 'email', 'phone', 'username', 'password', 'address']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email:
            # Validate định dạng email chuẩn
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                raise forms.ValidationError("Email is not valid")
            if Customer.objects.filter(email=email).exists():
                raise forms.ValidationError("Email already exists")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if phone:
            # Validate phone: chỉ số, có thể + ở đầu, độ dài 7-15
            if not re.match(r'^\+?\d{7,15}$', phone):
                raise forms.ValidationError("Phone number is not valid")
            if Customer.objects.filter(phone=phone).exists():
                raise forms.ValidationError("Phone already exists")
        return phone

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if username and Customer.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        # Hash password
        if password:
            cleaned_data['password'] = hash_password(password)

        return cleaned_data

# -----------------------
# Login Form
# -----------------------
class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            hashed = hash_password(password)
            try:
                customer = Customer.objects.get(username=username, password=hashed)
                cleaned_data['customer'] = customer
            except Customer.DoesNotExist:
                raise forms.ValidationError("Invalid username or password")

        return cleaned_data
