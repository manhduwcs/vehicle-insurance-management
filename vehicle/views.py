from django.shortcuts import render, get_object_or_404, redirect
from .models import VehicleType, Vehicle
from .forms import VehicleTypeForm, VehicleForm
from django.contrib.auth.decorators import login_required
from contracts.models import Contracts
from app_helper.views import notify
from accounts.decorators import customer_login_required, employee_login_required

# VehicleType CRUD

def vehicle_type_list(request):
    vehicle_types = VehicleType.objects.all().order_by('-id')
    context = {
        "vehicle_types": vehicle_types,
        "segment": "vehicle_type",
    }
    return render(request, "vehicle_types/list.html", context)

def vehicle_type_detail(request, pk):
    vehicle_type = get_object_or_404(VehicleType, pk=pk)
    context = {
        "vehicle_type": vehicle_type,
        "segment": "vehicle_type",
    }
    return render(request, "vehicle_types/detail.html", context)

def vehicle_type_create(request):
    if request.method == "POST":
        form = VehicleTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("vehicle_type_list")
    else:
        form = VehicleTypeForm()
    context = {
        "form": form,
        "segment": "vehicle_type",
    }
    return render(request, "vehicle_types/create.html", context)

def vehicle_type_update(request, pk):
    vehicle_type = get_object_or_404(VehicleType, pk=pk)
    if request.method == "POST":
        form = VehicleTypeForm(request.POST, instance=vehicle_type)
        if form.is_valid():
            form.save()
            return redirect("vehicle_type_detail", pk=vehicle_type.pk)
    else:
        form = VehicleTypeForm(instance=vehicle_type)
    context = {
        "vehicle_type": vehicle_type,
        "segment": "vehicle_type",
        "form": form
    }
    return render(request, "vehicle_types/update.html", context)

def vehicle_type_delete(request, pk):
    vehicle_type = get_object_or_404(VehicleType, pk=pk)
    if request.method == "POST":
        vehicle_type.delete()
    return redirect("vehicle_type_list")

# Vehicle CRUD

@customer_login_required
def vehicle_list(request):
    # Chỉ hiển thị vehicle của customer đang đăng nhập
    vehicles = Vehicle.objects.filter(customer=request.customer).order_by('-id')
    context = {
        "vehicles": vehicles,
        "segment": "vehicle",
    }
    return render(request, "vehicle/list.html", context)

@customer_login_required
def vehicle_detail(request, pk):
    # Chỉ cho phép xem vehicle của chính customer đó
    vehicle = get_object_or_404(Vehicle, pk=pk, customer=request.customer)
    context = {
        "vehicle": vehicle,
        "segment": "vehicle",
    }
    return render(request, "vehicle/detail.html", context)

@customer_login_required
def vehicle_create(request):
    if request.method == "POST":
        form = VehicleForm(request.POST)
        if form.is_valid():
            # Tự động gán customer từ session
            vehicle = form.save(commit=False)
            vehicle.customer = request.customer
            vehicle.save()
            return redirect("vehicle_list")
    else:
        form = VehicleForm()
    from .models import VehicleType
    vehicle_types = VehicleType.objects.all()
    context = {
        "form": form,
        "segment": "vehicle",
        "vehicle_types": vehicle_types
    }
    return render(request, "vehicle/create.html", context)

@customer_login_required
def vehicle_update(request, pk):
    # Chỉ cho phép sửa vehicle của chính customer đó
    vehicle = get_object_or_404(Vehicle, pk=pk, customer=request.customer)
    if request.method == "POST":
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            return redirect("vehicle_detail", pk=vehicle.pk)
    else:
        form = VehicleForm(instance=vehicle)
    from .models import VehicleType
    vehicle_types = VehicleType.objects.all()
    context = {
        "vehicle": vehicle,
        "segment": "vehicle",
        "form": form,
        "vehicle_types": vehicle_types
    }
    return render(request, "vehicle/update.html", context)

@customer_login_required
def vehicle_delete(request, pk):
    # Chỉ cho phép xóa vehicle của chính customer đó
    vehicle = get_object_or_404(Vehicle, pk=pk, customer=request.customer)
    if request.method == "POST":
        vehicle.delete()
        return redirect("vehicle_list")
    # if GET, render confirm page or redirect
    return redirect("vehicle_detail", pk=pk)

# NOTE: Claims views have been moved to the separate 'claims' app.
# If any old claim_* functions remain here, remove them to avoid duplication.
