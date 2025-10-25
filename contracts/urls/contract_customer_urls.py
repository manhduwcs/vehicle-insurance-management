from django.urls import path
from contracts.views.contract_customer_view import *

app_name = 'contracts_customer'

urlpatterns = [
    # show categories list (customer choose)
    path('list_categories/', list_insurance_categories, name='list_category'),

    # customer only!
    path('', contract_list, name='contract_list'),
    path('<int:pk>/', contract_detail, name='contract_detail'),
    path('<int:pk>/cancel', contract_cancel, name='contract_cancel'),
    path('<int:pk>/payment/', goto_payment_choice, name='contract_payment'),
    path('<int:pk>/payment/qr/', pay_with_qr, name='contract_payment_qr'),
    path('<int:pk>/payment/direct/', pay_direct, name='contract_payment_direct'),
    path('<int:pk>/payment/card/', pay_with_card, name='contract_payment_card'),
    path('<int:pk>/payment/detail/', payment_detail, name='contract_payment_detail'),

    path('contracts/create_civil/<int:category_id>/', create_contract_civil, name='create_contract_civil'),
    path('contracts/create_other/<int:category_id>/', create_contract_other, name='create_contract_other'),
    path('calculate/', calculate_insurance, name='calculate_insurance'),
]
