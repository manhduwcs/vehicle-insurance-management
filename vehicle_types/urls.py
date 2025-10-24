from django.urls import path
from . import views

app_name = 'vehicle_types'

urlpatterns = [
    path('', views.vehicle_type_list, name='vehicle_type_list'),
    path('create/', views.vehicle_type_create, name='vehicle_type_create'),
    path('update/<int:pk>/', views.vehicle_type_update, name='vehicle_type_update'),
    path('detail/<int:pk>/', views.vehicle_type_detail, name='vehicle_type_detail'),
    path('delete/<int:pk>/', views.vehicle_type_delete, name='vehicle_type_delete'),
]