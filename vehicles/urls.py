from django.urls import path
from . import views
from . import customer_view

app_name = 'vehicles'

urlpatterns = [
    # 
    path('', views.vehicle_list, name='vehicle_list'),
    path('create/', views.vehicle_create, name='vehicle_create'),
    path('update/<int:pk>/', views.vehicle_update, name='vehicle_update'),
    path('detail/emp/<int:pk>/', views.vehicle_detail_emp, name='vehicle_detail_emp'),
    path('detail/cus/<int:pk>/', views.vehicle_detail_cus, name='vehicle_detail_cus'),
    path('delete/<int:pk>/', views.vehicle_delete, name='vehicle_delete'),
    path('info/', views.vehicle_info, name='vehicle_info'),

    # customer only !
    path('customer/', customer_view.customer_vehicle_list, name='customer_vehicle_list'),
    path('customer/create/', customer_view.customer_vehicle_create, name='customer_vehicle_create'),
    path('customer/update/<int:pk>/', customer_view.customer_vehicle_update, name='customer_vehicle_update'),
    path('customer/detail/<int:pk>/', customer_view.customer_vehicle_detail, name='customer_vehicle_detail'),
    path('customer/delete/<int:pk>/', customer_view.customer_vehicle_delete, name='customer_vehicle_delete'),

]
