from django.urls import path
from contracts.views.contract_employee_views import *

app_name = 'contracts'

urlpatterns = [
    # employee only!
    # path('', contract_list, name='contract_list'),
    # path('<int:pk>/', contract_detail, name='contract_detail'),
    # path('<int:pk>/update/', contract_update, name='contract_update'),
    # path('<int:pk>/payment/', goto_payment_choice, name='contract_payment'),
]
