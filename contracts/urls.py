from django.urls import path
from .views import views, contract_employee_views

app_name = 'contracts'

urlpatterns = [
    path('list_categories/', contract_employee_views.list_insurance_categories, name='list'),


    # path('/payment/', contract_employee_views.go_to_payment, name='contract_payment'),
    # ---- employee only
    # employee view and manage all contracts
    # path('', contract_employee_views.contract_list, name='contract_list'),
    # path('<int:pk>/', contract_employee_views.contract_detail, name='contract_detail'),
    # path('<int:pk>/update/', contract_employee_views.contract_update, name='contract_update'),
    # path('<int:pk>/payment/', contract_employee_views.goto_payment_choice, name='contract_payment'),
    # path('<int:pk>/payment/qr/', contract_employee_views.pay_with_qr, name='contract_payment_qr'),
    # path('<int:pk>/payment/direct/', contract_employee_views.pay_direct, name='contract_payment_direct'),
    # path('<int:pk>/payment/card/', contract_employee_views.pay_with_card, name='contract_payment_card'),
    # path('<int:pk>/payment/detail/', contract_employee_views.payment_detail, name='contract_payment_detail'),


    # ---- customer only
    # show customer's contracts
    path('my_contracts/', views.contract_list_customer, name='contract_list_customer'),  
    path('contracts/create_civil/<int:category_id>/', views.create_contract_civil, name='create_contract_civil'),
    path('contracts/create_other/<int:category_id>/', views.create_contract_other, name='create_contract_other'),
    path('calculate/', views.calculate_insurance, name='calculate_insurance'),
]
