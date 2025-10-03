from django.shortcuts import render

def index(request):
    context = {
        "segment": "home",
        "title": "Welcome to My Site",
        "message": "This is the home page!"
    }
    return render(request, "home/index.html", context)