from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Vehicles, VehicleTypes
from .forms import VehicleForm
from employee.views import has_permission
from permissions.constants import FunctionIds, ActionIds

def customer_vehicle_list(request):
    if 'username' not in request.session:
        return redirect('accounts:login')

    user_id = request.session.get('user_id')
    group_id = request.session.get('group_id')

    if not has_permission(group_id, FunctionIds.ManageVehicle, ActionIds.View):
        messages.error(request, "You do not have permission to view vehicles.")
        return redirect('home')

    vehicles = Vehicles.objects.filter(customer_id=user_id).select_related('vehicle_type').order_by('-id')
    vehicle_types = VehicleTypes.objects.all()
    paginator = Paginator(vehicles, 10)  # 10 items per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return render(request, 'vehicles/customer_vehicles/list.html', {
        'vehicles': page_obj,
        'vehicle_types': vehicle_types,
        'can_add': has_permission(group_id, FunctionIds.ManageVehicle, ActionIds.Create),
        'can_edit': has_permission(group_id, FunctionIds.ManageVehicle, ActionIds.Edit),
        'can_delete': has_permission(group_id, FunctionIds.ManageVehicle, ActionIds.Delete),
    })

def customer_vehicle_detail(request, pk):
    if 'username' not in request.session:
        return redirect('accounts:login')

    group_id = request.session.get('group_id')
    if not has_permission(group_id, FunctionIds.ManageVehicle, ActionIds.View):
        messages.error(request, "You do not have permission to view vehicle details.")
        return redirect('vehicles:customer_vehicle_list')

    vehicle = get_object_or_404(Vehicles, pk=pk)
    return render(request, 'customer_vehicles/detail.html', {
        'vehicle': vehicle,
        'can_edit': has_permission(group_id, FunctionIds.ManageVehicle, ActionIds.Edit),
        'can_delete': has_permission(group_id, FunctionIds.ManageVehicle, ActionIds.Delete),
    })

def customer_vehicle_create(request):
    if 'username' not in request.session:
        return redirect('accounts:login')

    group_id = request.session.get('group_id')
    user_id = request.session.get('user_id')
    if not has_permission(group_id, FunctionIds.ManageVehicle, ActionIds.Create):
      
        messages.error(request, "You do not have permission to create vehicles.")
        return redirect('vehicles:customer_vehicle_list')

    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.customer_id_id = user_id
            vehicle.save()
            messages.success(request, 'Vehicle created successfully!')
            return redirect('vehicles:customer_vehicle_list')
        else:
            messages.error(request, form.errors.as_text())
    else:
        form = VehicleForm()

    return render(request, 'customer_vehicles/create.html', {'form': form})

def customer_vehicle_update(request, pk):
    if 'username' not in request.session:
        return redirect('accounts:login')

    group_id = request.session.get('group_id')
    if not has_permission(group_id, FunctionIds.ManageVehicle, ActionIds.Edit):
        messages.error(request, "You do not have permission to edit vehicles.")
        return redirect('vehicles:customer_vehicle_list')

    vehicle = get_object_or_404(Vehicles, pk=pk)

    if request.method == 'POST':
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vehicle updated successfully!')
            return redirect('vehicles:customer_vehicle_list')
        else:
            messages.error(request, form.errors.as_text())
    else:
        form = VehicleForm(instance=vehicle)

    return render(request, 'customer_vehicles/update.html', {'form': form, 'vehicle': vehicle})

def customer_vehicle_delete(request, pk):
    if 'username' not in request.session:
        return redirect('accounts:login')

    group_id = request.session.get('group_id')
    if not has_permission(group_id, FunctionIds.ManageVehicle, ActionIds.Delete):
        messages.error(request, "You do not have permission to delete vehicles.")
        return redirect('vehicles:customer_vehicle_list')

    vehicle = get_object_or_404(Vehicles, pk=pk)
    if request.method == 'POST':
        vehicle.delete()
        messages.success(request, 'Vehicle deleted successfully!')
        return redirect('vehicles:customer_vehicle_list')

    return redirect('vehicles:customer_vehicle_list')
