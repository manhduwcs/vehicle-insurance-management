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
