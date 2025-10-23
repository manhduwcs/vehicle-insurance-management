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
    path("home-customer/", views.home_page_customer, name="home-customer"),
    path("about/", views.about, name="about"),
    path('contact/', views.contact, name="contact"),
    path('services/', views.services, name="services")
]