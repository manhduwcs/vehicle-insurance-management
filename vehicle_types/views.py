from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import VehicleTypes
from .forms import VehicleTypeForm
from employee.views import has_permission
from permissions.constants import FunctionIds, ActionIds


def vehicle_type_list(request):
    if "username" not in request.session:
        return redirect("employee:login")
    group_id = request.session.get("group_id", None)
    if not has_permission(group_id, FunctionIds.ManageVehicleTypes, ActionIds.View):
        messages.error(request, "You do not have permission to view the vehicle types list.")
        return redirect("home")

    vehicle_types = VehicleTypes.objects.all().order_by('id')
    return render(request, 'vehicle_types/list.html', {
        'vehicle_types': vehicle_types,
        'can_add': has_permission(group_id, FunctionIds.ManageVehicleTypes, ActionIds.Create),
        'can_edit': has_permission(group_id, FunctionIds.ManageVehicleTypes, ActionIds.Edit),
        'can_delete': has_permission(group_id, FunctionIds.ManageVehicleTypes, ActionIds.Delete),
        'segment': 'vehicle_types',
    })


def vehicle_type_create(request):
    if 'username' not in request.session:
        return redirect('employee:login')
    user_group_id = request.session.get('group_id', None)
    if not has_permission(user_group_id, FunctionIds.ManageVehicleTypes, ActionIds.Create):
        messages.error(request, "You do not have permission to create vehicle types.")
        return redirect('vehicle_types:vehicle_type_list')

    if request.method == 'POST':
        form = VehicleTypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vehicle type created successfully!')
            return redirect('vehicle_types:vehicle_type_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = VehicleTypeForm()
    return render(request, 'vehicle_types/create.html', {'form': form, 'segment': 'vehicle_types'})


def vehicle_type_update(request, pk):
    if 'username' not in request.session:
        return redirect('employee:login')
    user_group_id = request.session.get('group_id', None)
    if not has_permission(user_group_id, FunctionIds.ManageVehicleTypes, ActionIds.Edit):
        messages.error(request, "You do not have permission to edit vehicle types.")
        return redirect('vehicle_types:vehicle_type_list')

    vehicle_type = get_object_or_404(VehicleTypes, pk=pk)
    if request.method == 'POST':
        form = VehicleTypeForm(request.POST, instance=vehicle_type)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vehicle type updated successfully!')
            return redirect('vehicle_types:vehicle_type_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = VehicleTypeForm(instance=vehicle_type)
    return render(request, 'vehicle_types/update.html', {'form': form, 'vehicle_type': vehicle_type, 'segment': 'vehicle_types'})


def vehicle_type_detail(request, pk):
    if 'username' not in request.session:
        return redirect('employee:login')
    user_group_id = request.session.get('group_id', None)
    if not has_permission(user_group_id, FunctionIds.ManageVehicleTypes, ActionIds.View):
        messages.error(request, "You do not have permission to view vehicle type details.")
        return redirect('vehicle_types:vehicle_type_list')

    vehicle_type = get_object_or_404(VehicleTypes, pk=pk)
    return render(request, 'vehicle_types/detail.html', {
        'vehicle_type': vehicle_type,
        'can_edit': has_permission(user_group_id, FunctionIds.ManageVehicleTypes, ActionIds.Edit),
        'can_delete': has_permission(user_group_id, FunctionIds.ManageVehicleTypes, ActionIds.Delete),
        'segment': 'vehicle_types',
    })


def vehicle_type_delete(request, pk):
    if 'username' not in request.session:
        return redirect('employee:login')
    user_group_id = request.session.get('group_id', None)
    if not has_permission(user_group_id, FunctionIds.ManageVehicleTypes, ActionIds.Delete):
        messages.error(request, "You do not have permission to delete vehicle types.")
        return redirect('vehicle_types:vehicle_type_list')

    vehicle_type = get_object_or_404(VehicleTypes, pk=pk)
    if request.method == 'POST':
        vehicle_type.delete()
        messages.success(request, 'Vehicle type deleted successfully!')
        return redirect('vehicle_types:vehicle_type_list')
    return redirect('vehicle_types:vehicle_type_list')