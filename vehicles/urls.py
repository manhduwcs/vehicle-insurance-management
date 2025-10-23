from django.urls import path
from . import views

app_name = 'vehicles'

urlpatterns = [
    path('', views.vehicle_list, name='vehicle_list'),
    path('create/', views.vehicle_create, name='vehicle_create'),
    path('update/<int:pk>/', views.vehicle_update, name='vehicle_update'),
    path('detail/emp/<int:pk>/', views.vehicle_detail_emp, name='vehicle_detail_emp'),
    path('detail/cus/<int:pk>/', views.vehicle_detail_cus, name='vehicle_detail_cus'),
    path('delete/<int:pk>/', views.vehicle_delete, name='vehicle_delete'),
    path('info/', views.vehicle_info, name='vehicle_info'),
]