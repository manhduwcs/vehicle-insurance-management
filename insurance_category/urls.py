from django.urls import path
from . import views

app_name = 'insurance_category'

urlpatterns = [
    path("", views.insurance_category_list, name="insurance_category_list"),
    path("<int:pk>/", views.insurance_category_detail, name="insurance_category_detail"),
    path("create/", views.insurance_category_create, name="insurance_category_create"),
    path("<int:pk>/update/", views.insurance_category_update, name="insurance_category_update"),
    path("<int:pk>/delete/", views.insurance_category_delete, name="insurance_category_delete"),
]
