from functools import wraps
from django.shortcuts import redirect

def customer_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not getattr(request, 'customer', None):
            return redirect('accounts:login')
        return view_func(request, *args, **kwargs)
    return wrapper
