from django.urls import path
from .views import views, contract_employee_views

app_name = 'contracts'

urlpatterns = [
    path('list_categories/', views.list_insurance_categories, name='list'),


    # ---- employee only
    # employee view and manage all contracts
    path('', contract_employee_views.contract_list, name='contract_list'),
    path('<int:pk>/', contract_employee_views.contract_detail, name='contract_detail'),
    path('<int:pk>/update/', contract_employee_views.contract_update, name='contract_update'),
    path('<int:pk>/payment/', contract_employee_views.go_to_payment, name='contract_payment'),


    # ---- customer only
    # show customer's contracts
    path('my_contracts/', views.contract_list_customer, name='contract_list_customer'),  
    path('contracts/create_civil/<int:category_id>/', views.create_contract_civil, name='create_contract_civil'),
    path('contracts/create_other/<int:category_id>/', views.create_contract_other, name='create_contract_other'),
    path('calculate/', views.calculate_insurance, name='calculate_insurance'),
]
