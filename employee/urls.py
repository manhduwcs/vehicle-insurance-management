# employee/urls.py
from django.urls import path
from .views import (
    employee_list, employee_create, employee_update, employee_delete, employee_detail, login_view
)

app_name = 'employee'

urlpatterns = [
    path('', employee_list, name='employee_list'),
    path('create/', employee_create, name='employee_create'),
    path('update/<int:pk>/', employee_update, name='employee_update'),
    path('delete/<int:pk>/', employee_delete, name='employee_delete'),
    path('detail/<int:pk>/', employee_detail, name='employee_detail'),
    path('login/', login_view, name='login'),
]