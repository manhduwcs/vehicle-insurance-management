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
    Middleware này sẽ chặn người dùng đã đăng nhập (qua session)
    khỏi truy cập vào các trang login/register.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_id = request.session.get('user_id')
        path = request.path

        # Danh sách các URL cần chặn nếu đã login
        protected_paths = [
            reverse('accounts:login'),
            reverse('accounts:register'),
        ]

        # Nếu user đã login mà vẫn vào login/register => redirect
        if user_id and any(path.startswith(p) for p in protected_paths):
            return redirect('home')

        # Cho phép request bình thường
        response = self.get_response(request)
        return response