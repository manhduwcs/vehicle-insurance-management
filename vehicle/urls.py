from django.urls import path
from . import views

urlpatterns = [
    path('vehicle-types/', views.vehicle_type_list, name='vehicle_type_list'),
    path('vehicle-types/<int:pk>/', views.vehicle_type_detail, name='vehicle_type_detail'),
    path('vehicle-types/create/', views.vehicle_type_create, name='vehicle_type_create'),
    path('vehicle-types/<int:pk>/update/', views.vehicle_type_update, name='vehicle_type_update'),
    path('vehicle-types/<int:pk>/delete/', views.vehicle_type_delete, name='vehicle_type_delete'),
    path('vehicles/', views.vehicle_list, name='vehicle_list'),
    path('vehicles/<int:pk>/', views.vehicle_detail, name='vehicle_detail'),
    path('vehicles/create/', views.vehicle_create, name='vehicle_create'),
    path('vehicles/<int:pk>/update/', views.vehicle_update, name='vehicle_update'),
    path('vehicles/<int:pk>/delete/', views.vehicle_delete, name='vehicle_delete'),
]
