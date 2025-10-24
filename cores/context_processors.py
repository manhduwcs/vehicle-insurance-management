from .services.permissions import get_accessible_functions

def sidebar_permissions(request):
    functions = get_accessible_functions(request)
    return {'accessible_functions': functions}
