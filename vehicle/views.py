from django.shortcuts import render, get_object_or_404, redirect
from .models import VehicleType, Vehicle
from .forms import VehicleTypeForm, VehicleForm

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
            return redirect("vehicle_type_list")
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
    return redirect("vehicle_type_list")

# Vehicle CRUD

def vehicle_list(request):
    vehicles = Vehicle.objects.all().order_by('-id')
    context = {
        "vehicles": vehicles,
        "segment": "vehicle",
    }
    return render(request, "vehicles/list.html", context)

def vehicle_detail(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    context = {
        "vehicle": vehicle,
        "segment": "vehicle",
    }
    return render(request, "vehicles/detail.html", context)

def vehicle_create(request):
    if request.method == "POST":
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("vehicle_list")
    else:
        form = VehicleForm()
    from admin_soft.models import Customer
    from .models import VehicleType
    customers = Customer.objects.all()
    vehicle_types = VehicleType.objects.all()
    context = {
        "form": form,
        "segment": "vehicle",
        "customers": customers,
        "vehicle_types": vehicle_types
    }
    return render(request, "vehicles/create.html", context)

def vehicle_update(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    if request.method == "POST":
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            return redirect("vehicle_list")
    else:
        form = VehicleForm(instance=vehicle)
    from admin_soft.models import Customer
    from .models import VehicleType
    customers = Customer.objects.all()
    vehicle_types = VehicleType.objects.all()
    context = {
        "vehicle": vehicle,
        "segment": "vehicle",
        "form": form,
        "customers": customers,
        "vehicle_types": vehicle_types
    }
    return render(request, "vehicles/update.html", context)

def vehicle_delete(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    if request.method == "POST":
        vehicle.delete()
        return redirect("vehicle_list")
    return redirect("vehicle_list")
