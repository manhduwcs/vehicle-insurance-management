from django.urls import path
from .views import views, contract_employee_views

app_name = 'contracts'

urlpatterns = [
    path('categories/', views.list_insurance_categories, name='list'),
    path('contracts/<int:pk>/', contract_employee_views.contract_detail, name='contract_detail'),
    path('contracts/<int:pk>/update/', contract_employee_views.contract_update, name='contract_update'),

    path('contracts/create_civil/<int:category_id>/', views.create_contract_civil, name='create_contract_civil'),
    path('contracts/create_other/<int:category_id>/', views.create_contract_other, name='create_contract_other'),
    path('contracts/calculate/', views.calculate_insurance, name='calculate_insurance'),
    path('contracts/', views.contract_list, name='contract_list'),
]
