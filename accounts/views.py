from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm, LoginForm

# -------------------
# REGISTER
# -------------------
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. Please login.")
            return redirect('accounts:login')
        else:
            messages.error(request, form.errors)
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

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
            messages.success(request, f"Welcome, {customer.fullname}!")
            return redirect('home')
        else:
            messages.error(request, form.errors)
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

# -------------------
# LOGOUT
# -------------------
def logout_view(request):
    request.session.flush()
    messages.success(request, "You have logged out successfully.")
    return redirect('accounts:login')
