from django.shortcuts import redirect
from django.urls import reverse
from customer.models import Customer

class CustomerAuthMiddleware:
    """
    Attach customer object vào request
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.customer = None
        user_id = request.session.get('user_id')
        user_type = request.session.get('user_type')
        if user_id and user_type == 'customer':
            try:
                request.customer = Customer.objects.get(id=user_id)
            except Customer.DoesNotExist:
                request.customer = None
        return self.get_response(request)


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
            return redirect('home')

        # Allow normal request processing
        response = self.get_response(request)
        return response