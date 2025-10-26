from .services.permissions import get_accessible_functions

def sidebar_permissions(request):
    functions = get_accessible_functions(request)
    return {'accessible_functions': functions}


def customer_context(request):
    """
    Inject customer info into all templates if logged in.
    """
  
    customer = request.user

    return {
        'customer': customer
    }