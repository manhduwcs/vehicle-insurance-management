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
                request.session.set_expiry(7 * 24 * 60 * 60)  
            else:
                request.session.set_expiry(0)  
            messages.success(request, f"Welcome, {customer.fullname}!")
            return redirect('home')
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
    messages.success(request, "You have logged out successfully.")
    return redirect('accounts:login')
