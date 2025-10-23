from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm, LoginForm, UserPasswordResetForm,UserSetPasswordForm
from django.contrib.auth.hashers import make_password
from app_helper.views import notify
from permissions.models import GroupsUsers 
from customer.models import Customer
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.conf import settings
from .tokens import customer_token_generator as default_token_generator
from django.urls import reverse
from django.core.mail import send_mail

# -------------------
# REGISTER
# -------------------
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            default_group = GroupsUsers.objects.get(id=2)
            customer.group_id = default_group
            customer.save()
            notify(request,"Registration successful. Please login.",'success')
            return redirect('accounts:login')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

# -------------------
# LOGIN
# -------------------
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            
            customer = form.cleaned_data['customer']
            request.session['user_id'] = customer.id
            request.session['user_type'] = 'customer'
            request.session['username'] = customer.username
            remember_me = request.POST.get('remember_me')
            if remember_me == 'on':
                request.session.set_expiry(7 * 24 * 60 * 60)  # 7 days
            else:
                request.session.set_expiry(86400)  # 24 hours instead of 0  
            notify(request, f"Welcome, {customer.fullname}!", 'success')
            return redirect('home-customer')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})

# -------------------
# LOGOUT
# -------------------
def logout_view(request):
    request.session.flush()
    notify(request, "You have logged out successfully.", 'success')
    return redirect('home-customer')



def reset_password_view(request):
    if request.method == "POST":
        form = UserPasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            customer = Customer.objects.get(email=email)

           
            uid = urlsafe_base64_encode(force_bytes(customer.pk))
            token = default_token_generator.make_token(customer)

           
            reset_url = request.build_absolute_uri(
                reverse('accounts:password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
            )

            expiry_time_minutes = int(getattr(settings, 'PASSWORD_RESET_TIMEOUT', 300) / 60)
            
            subject = "Password Reset Request"
            message = f"""Hi {customer.fullname},

            You requested to reset your password. Click the link below to reset it:

            {reset_url}

            This link will expire in {expiry_time_minutes:.0f} minute(s).

            If you didn't request this, please ignore this email.

            Best regards,
            Your Team"""
            from_email = "no-reply@yourapp.com"

            send_mail(subject, message, from_email, [email])

            messages.success(request, "A password reset link has been sent to your email.")
            return redirect('accounts:password_change_done')
    else:
        form = UserPasswordResetForm()

    return render(request, 'accounts/password_reset.html', {'form': form})

def password_reset_done_view(request):
    return render(request, 'accounts/password_reset_done.html')


def password_reset_confirm_view(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        customer = Customer.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Customer.DoesNotExist):
        customer = None

    if customer is not None and default_token_generator.check_token(customer, token):
        if request.method == "POST":
            form = UserSetPasswordForm(customer, request.POST)
            if form.is_valid():
                new_password = form.cleaned_data["new_password1"]
                customer.password = make_password(new_password)
                customer.save()
                messages.success(request, "Your password has been reset successfully.")
                return redirect("accounts:login")
        else:
            form = UserSetPasswordForm(customer)
        return render(request, "accounts/password_reset_confirm.html", {"form": form, "validlink": True})
    else:
        messages.error(request, "The password reset link is invalid or has expired.")
        return render(request, "accounts/password_reset_confirm.html", {"validlink": False})