from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from accounts.decorators import customer_login_required
from contracts.forms import ContractForm
from permissions.views import has_permission
from dateutil.relativedelta import relativedelta
from datetime import datetime
from django.db.models import Q
from vehicles.models import Vehicles
from categories.models import Duration, InsuranceCategories, InsurancePriceList
from contracts.models import Contracts, Depreciations
from vehicle_types.models import VehicleTypes
from decimal import Decimal


