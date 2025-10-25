# employee/urls.py
from django.urls import path
from .views import (
    employee_list,
    employee_create,
    employee_update,
    employee_delete,
    employee_detail,
    employee_profile,
    change_password,
    login_view,
    reset_password_view,
    password_reset_confirm_view,
    password_reset_done_view
)

app_name = 'employee'

urlpatterns = [
    path('', employee_list, name="employee_list"),
    path('create/', employee_create, name='employee_create'),
    path('update/<int:pk>/', employee_update, name='employee_update'),
    path('delete/<int:pk>/', employee_delete, name='employee_delete'),
    path('detail/<int:pk>/', employee_detail, name='employee_detail'),
    path('profile/', employee_profile, name='profile'),
    path('change-password/', change_password, name='change_password'),
    path('login/', login_view, name='login'),
    path('reset-password/', reset_password_view, name='reset_password'),
    path('password-reset-confirm/<uidb64>/<token>/', password_reset_confirm_view, name='password_reset_confirm'),
    path('password-change/', password_reset_confirm_view, name='password_change'),
    path('password-change-done/', password_reset_done_view, name='password_change_done'),

]
