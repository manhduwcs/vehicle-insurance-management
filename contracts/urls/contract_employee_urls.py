from django.urls import path
from contracts.views.contract_employee_views import *

app_name = 'contracts_employee'

urlpatterns = [
    # employee only!
    path('', contract_list, name='contract_list'),
    path('<int:pk>/', contract_detail, name='contract_detail'),
    path('<int:pk>/update/', contract_update, name='contract_update'),
    path('<int:pk>/reject/', contract_reject, name='contract_reject'),
    path('<int:pk>/payment_detail/', payment_detail, name='contract_payment_detail'),
]
