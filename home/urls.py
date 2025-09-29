from django.http import HttpResponse
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path('', lambda r: HttpResponse("Index placeholder"), name="index"),
    path('', lambda r: HttpResponse("Index placeholder"), name="tables"),
    path('', lambda r: HttpResponse("Index placeholder"), name="billing"),
    path('', lambda r: HttpResponse("Index placeholder"), name="vr"),
    path('', lambda r: HttpResponse("Index placeholder"), name="rtl"),
    path('', lambda r: HttpResponse("Index placeholder"), name="login"),
    path('', lambda r: HttpResponse("Index placeholder"), name="register"),
]