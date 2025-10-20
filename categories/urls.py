from django.urls import path
from . import views

app_name = 'categories'

urlpatterns = [
    path('', views.category_list, name='category_list'),
    path('create/', views.category_create, name='category_create'),
    path('update/<int:pk>/', views.category_update, name='category_update'),
    path('delete/<int:pk>/', views.category_delete, name='category_delete'),
    path('edit-price-list/', views.edit_price_list, name='edit_price_list'),
    path('update-max-coverage/', views.update_max_coverage, name='update_max_coverage'),
]