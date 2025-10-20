from django.urls import path
from . import views

urlpatterns = [
    path('', views.claim_list, name='claim_list'),
    path('create/', views.claim_create, name='claim_create'),
    path('<int:pk>/', views.claim_detail, name='claim_detail'),
    path('<int:pk>/update/', views.claim_update, name='claim_update'),
    path('ajax/contracts/<int:vehicle_id>/', views.contracts_for_vehicle, name='ajax_contracts_for_vehicle'),
]