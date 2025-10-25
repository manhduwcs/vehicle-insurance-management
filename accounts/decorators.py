# decorators.py
from functools import wraps
from django.shortcuts import redirect

from permissions.models import GroupsFunctionsActions
from django.core.cache import cache
from app_helper.views import notify
def has_permission(group, function_name, action_name):
    if not group:
        return False

    
    cache_key = f"perm_{group.id}_{function_name}_{action_name}"
    perm = cache.get(cache_key)

    if perm is None:
        perm = GroupsFunctionsActions.objects.filter(
            group=group,
            function__function_name=function_name,
            action__action_name=action_name
        ).exists()
        cache.set(cache_key, perm, timeout=3600)  

    return perm

def permission_required(function_name, action_name):
    """
    Check if current user (any type) has permission by group_id
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            user_id = request.session.get("user_id")
            if not user_id:
                notify(request, "Please log in first.", "error")
                return redirect("home-customer")

            group_id = request.session.get("group_id")
            if not group_id:
                notify(request, "Your account is not assigned to any group.", "error")
                return redirect("home-customer")

            if not has_permission(group_id, function_name, action_name):
                notify(request, "You do not have permission to access this feature.", "error")
                return redirect("home-customer")

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator