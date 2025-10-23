"""
URL configuration for vehicle_insurance_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from employee.views import login_view
from django.conf import settings
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('permissions/', include('permissions.urls')),
    path('employees/', include('employee.urls')),
    path('login/', login_view, name='login'),
    path('', include('home.urls')),
    path('discount/', include('discount.urls')),
    path('expenses/', include('expenses.urls')),
    path('customers/', include('customer.urls')),
    path('accounts/', include('accounts.urls')),
    path('vehicles/', include('vehicles.urls')),
    path('vehicle_types/', include('vehicle_types.urls')),
    path('claims/', include('claims.urls')),
    path('categories/', include('categories.urls')),
    path('contracts/customer/', include('contracts.urls.contract_customer_urls', namespace='contracts_customer')),
    path('contracts/employee/', include('contracts.urls.contract_employee_urls', namespace='contracts_employee')),
]

# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
