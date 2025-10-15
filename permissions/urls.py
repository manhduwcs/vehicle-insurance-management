from django.urls import path
from . import views

app_name = 'permissions'

urlpatterns = [
    path('', views.groups_list, name='groups_list'),
    path('add/', views.add_group, name='add_group'),
    path('edit/<int:group_id>/', views.edit_group, name='edit_group'),
    path('delete/<int:group_id>/', views.delete_group, name='delete_group'),
    path('permission/<int:group_id>/', views.assign_permission, name='assign_permission'),
]