from django.shortcuts import redirect
from django.urls import reverse
from customer.models import Customer
from employee.models import Employees
from django.utils.deprecation import MiddlewareMixin

class UserAuthMiddleware(MiddlewareMixin):
    """
    Attach user object (employee/customer/admin) to request
    """
    def process_request(self, request):
        request.user = None
        request.group_id = None

        user_id = request.session.get('user_id')
        group_id = request.session.get('group_id')
        if hasattr(group_id, 'group_name'):
            group_id = group_id.group_name
        
        if not user_id:
            return 

        
        model_map = {
            "Employee": Employees,
            "Customer": Customer,
        }
        
        model = model_map.get(str(group_id))

        if model:
            try:
                user = model.objects.get(id=user_id)
                request.user = user
                request.group_id = group_id
            except model.DoesNotExist:
                request.user = None


class RedirectAuthenticatedUserMiddleware:
    """
    Middleware to redirect authenticated users away from login/register pages.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_id = request.session.get('user_id')
        path = request.path

        # The list of paths that should be protected from authenticated users
        protected_paths = [
            reverse('accounts:login'),
            reverse('accounts:register'),
        ]

        # If the user is logged in and tries to access login/register => redirect
        if user_id and any(path.startswith(p) for p in protected_paths):
            return redirect('home-customer')

        # Allow normal request processing
        response = self.get_response(request)
        return response