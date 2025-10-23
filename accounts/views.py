from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm, LoginForm
from django.contrib.auth.hashers import check_password
from app_helper.views import notify
from permissions.models import GroupsUsers  
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
