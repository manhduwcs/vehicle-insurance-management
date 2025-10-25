from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Vehicles, VehicleTypes
from .forms import VehicleForm
from employee.views import has_permission
from permissions.constants import FunctionIds, ActionIds
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator

def vehicle_list(request):
    if "username" not in request.session:
        return redirect("employee:login")
    group_id = request.session.get("group_id", None)
    if not has_permission(group_id, FunctionIds.ManageVehicle, ActionIds.View):
        messages.error(request, "You do not have permission to view the vehicles list.")
        return redirect("home")

    # Get params
    search = request.GET.get('search', '')
    vehicle_type_id = request.GET.get('vehicle_type_id', '')
    page = request.GET.get('page', 1)

    # Query vehicles with select_related for optimization
    vehicles = Vehicles.objects.select_related('customer_id', 'vehicle_type')

    # Query
    if search:
        vehicles = vehicles.filter(
            Q(customer_id__fullname__icontains=search) |
            Q(customer_id__phone__icontains=search) |
            Q(number__icontains=search)
        )

    # filter by vehicle_type
    if vehicle_type_id:
        vehicles = vehicles.filter(vehicle_type_id=vehicle_type_id)

    # Add order_by to fix UnorderedObjectListWarning
    vehicles = vehicles.order_by('-id')  # Sort by ID newest

    # Pagination
    paginator = Paginator(vehicles, 10)  # 10 items/page
    page_obj = paginator.get_page(page)

    # Get vehicle types list for dropdown
    vehicle_types = VehicleTypes.objects.all()

    # get permission to pass into context
    can_edit = has_permission(group_id, FunctionIds.ManageVehicle, ActionIds.Edit)
    can_delete = has_permission(group_id, FunctionIds.ManageVehicle, ActionIds.Delete)
    can_add = has_permission(group_id, FunctionIds.ManageVehicle, ActionIds.Create)

    # AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        table_body = render(request, 'vehicles/_table_body.html', {
            'vehicles': page_obj,
            'can_edit': can_edit,
            'can_delete': can_delete,
        }).content.decode('utf-8')
        pagination = render(request, 'vehicles/_pagination.html', {'page_obj': page_obj}).content.decode('utf-8')
        return JsonResponse({
            'table_body': table_body,
            'pagination': pagination,
        })

    # Render full page
    return render(request, 'vehicles/list.html', {
        'vehicles': page_obj,
        'vehicle_types': vehicle_types,
        'search': search,
        'selected_vehicle_type': vehicle_type_id,
        'can_add': can_add,
        'can_edit': can_edit,
        'can_delete': can_delete,
    })

def vehicle_detail_emp(request, pk):
    if "username" not in request.session:
        return redirect("employee:login")
    group_id = request.session.get("group_id", None)
    if not has_permission(group_id, FunctionIds.ManageVehicle, ActionIds.View):
        messages.error(request, "You do not have permission to view vehicle details.")
        return redirect("vehicles:vehicle_list")

    vehicle = get_object_or_404(Vehicles, pk=pk)
    return render(request, 'vehicles/detail.html', {
        'vehicle': vehicle,
    })

def vehicle_detail_cus(request, pk):
    if "username" not in request.session:
        return redirect("accounts:login")
    group_id = request.session.get("group_id", None)
    if not has_permission(group_id, FunctionIds.ManageVehicle, ActionIds.View):
        messages.error(request, "You do not have permission to view vehicle details.")
        return redirect("vehicles:vehicle_info")

    vehicle = get_object_or_404(Vehicles, pk=pk)
    return render(request, 'vehicles/detail.html', {
        'vehicle': vehicle,
        'can_edit': has_permission(group_id, FunctionIds.ManageVehicle, ActionIds.Edit),
        'can_delete': has_permission(group_id, FunctionIds.ManageVehicle, ActionIds.Delete),
    })

def vehicle_create(request):
    if 'username' not in request.session:
        return redirect('accounts:login')
    user_group_id = request.session.get('group_id', None)
    if not has_permission(user_group_id, FunctionIds.ManageVehicle, ActionIds.Create):
        messages.error(request, "You do not have permission to create vehicles.")
        return redirect('vehicles:vehicle_info')

    user_id = request.session.get('user_id', None)
    if user_id is None:
        messages.error(request, "User ID not found in session.")
        return redirect('employee:login')

    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.customer_id = user_id
            vehicle.save()
            messages.success(request, 'Vehicle created successfully!')
            return redirect('vehicles:vehicle_info')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = VehicleForm()
    return render(request, 'vehicles/create.html', {'form': form})

def vehicle_update(request, pk):
    if 'username' not in request.session:
        return redirect('accounts:login')
    user_group_id = request.session.get('group_id', None)
    if not has_permission(user_group_id, FunctionIds.ManageVehicle, ActionIds.Edit):
        messages.error(request, "You do not have permission to edit vehicles.")
        return redirect('vehicles:vehicle_info')

    vehicle = get_object_or_404(Vehicles, pk=pk)
    if request.method == 'POST':
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vehicle updated successfully!')
            return redirect('vehicles:vehicle_info')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = VehicleForm(instance=vehicle)
    return render(request, 'vehicles/update.html', {'form': form, 'vehicle': vehicle})

def vehicle_delete(request, pk):
    if 'username' not in request.session:
        return redirect('accounts:login')
    user_group_id = request.session.get('group_id', None)
    if not has_permission(user_group_id, FunctionIds.ManageVehicle, ActionIds.Delete):
        messages.error(request, "You do not have permission to delete vehicles.")
        return redirect('vehicles:vehicle_info')

    vehicle = get_object_or_404(Vehicles, pk=pk)
    if request.method == 'POST':
        vehicle.delete()
        messages.success(request, 'Vehicle deleted successfully!')
        return redirect('vehicles:vehicle_list')
    return redirect('vehicles:vehicle_info')

def vehicle_info(request):
    if 'username' not in request.session:
        return redirect('accounts:login')
    user_id = request.session.get('user_id', None)
    if user_id is None:
        messages.error(request, "User ID not found in session.")
        return redirect('accounts:login')

    group_id = request.session.get("group_id", None)
    if not has_permission(group_id, FunctionIds.ManageVehicle, ActionIds.View):
        messages.error(request, "You do not have permission to view your vehicles.")
        return redirect("home")

    vehicles = Vehicles.objects.filter(customer_id=user_id)
    return render(request, 'vehicles/info.html', {
        'vehicles': vehicles,
        'can_edit': has_permission(group_id, FunctionIds.ManageVehicle, ActionIds.Edit),
        'can_delete': has_permission(group_id, FunctionIds.ManageVehicle, ActionIds.Delete),
    })