from django.urls import path
from . import views

app_name = 'expenses'

urlpatterns = [
    path('', views.expense_list, name='expense_list'),
    path('create/', views.expense_create, name='expense_create'),
    path('update/<int:pk>/', views.expense_update, name='expense_update'),
    path('detail/<int:pk>/', views.expense_detail, name='expense_detail'),
    path('delete/<int:pk>/', views.expense_delete, name='expense_delete'),
]