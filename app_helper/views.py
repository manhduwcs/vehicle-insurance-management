from django.contrib import messages

def notify(request, message, status='info'):
    """
    Add a notification message to the Django messages framework.

    status can be: 'success', 'error', 'info', 'warning'
    """
    status_map = {
        'success': messages.SUCCESS,
        'error': messages.ERROR,
        'info': messages.INFO,
        'warning': messages.WARNING
    }
    level = status_map.get(status, messages.INFO)
    messages.add_message(request, level, message)

# Create your views here.
