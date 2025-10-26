from django.urls import path
from . import views

urlpatterns = [
    path('customer/', views.claim_list, name='claim_list'),
    path('customer/create/', views.claim_create, name='claim_create'),
    path('customer/<int:pk>/', views.claim_detail_customer, name='claim_detail'),
    path('customer/<int:pk>/status/<str:action>/', views.claim_update_status, name='claim_update_status'),
    path('customer/<int:pk>/update/', views.claim_update, name='claim_update'),
    path('ajax/contracts/<int:vehicle_id>/', views.contracts_for_vehicle, name='ajax_contracts_for_vehicle'),
    path('ajax/vehicle/<int:contract_id>/', views.vehicle_for_contract, name='ajax_vehicle_for_contract'),
    path('employee/', views.claims_list_admin, name='claim_list_admin'),
    path('employee/<int:pk>/', views.claim_detail_admin, name='claim_detail_admin'),
    path('employee/<int:pk>/approve/', views.claim_approve, name='claim_approve'),
]