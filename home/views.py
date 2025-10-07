from django.shortcuts import render
from accounts.decorators import customer_login_required

@customer_login_required
def index(request):
    context = {
        "segment": "home",
        "title": "Welcome to My Site",
        "message": "This is the home page!"
    }
    return render(request, "home/index.html", context)