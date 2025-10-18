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
from vehicle.models import Vehicle, VehicleType
from categories.models import Duration
from contracts.models import Contracts



@customer_login_required
def list_insurance_categories(request):
    if not has_permission(group_id=2, function_id=4, action_id=2):  # ManageContracts, Create
        messages.error(request, "You do not have permission to create contract.")
        return redirect("contracts:contract_list")

    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        vehicles = Vehicle.objects.filter(customer_id=request.session['user_id'])
        if not vehicles.exists():
            messages.error(request, "You need to register your vehicle on the system before purchasing insurance.")
            return render(request, 'categories/list.html', {'categories': InsuranceCategories.objects.all()})
        if category_id == '1':
            return redirect('contracts:create_contract_civil', category_id=category_id)
        return redirect('contracts:create_contract_other', category_id=category_id)

    return render(request, 'categories/list.html', {
        'categories': InsuranceCategories.objects.all()
    })


@customer_login_required
def create_contract_civil(request, category_id):
    if not has_permission(group_id=2, function_id=4, action_id=2):
        messages.error(request, "You do not have permission to create contract.")
        return redirect("contracts:contract_list")

    customer_id = request.session['user_id']
    form = ContractForm(customer_id=customer_id)
    durations = Duration.objects.all()

    if request.method == 'POST':
        form = ContractForm(request.POST, customer_id=customer_id)
        if form.is_valid():
            vehicle = form.cleaned_data['vehicle_id']
            duration_id = form.cleaned_data['duration_id']
            insurance_category_id = form.cleaned_data['insurance_category_id']

            # Calculate EstimatePremium
            vehicle_type = vehicle.vehicle_type
            price_list = InsurancePriceList.objects.filter(
                InsuranceCategoryID_id=insurance_category_id,
                DurationID_id=duration_id.id
            ).first()
            if not price_list:
                messages.error(request, "No insurance available for this vehicle age and duration.")
                return render(request, 'contracts/create_civil.html', {
                    'form': form,
                    'durations': durations,
                    'category': InsuranceCategories.objects.get(id=category_id)
                })

            estimate_premium = (vehicle_type.Fee * price_list.Rate) / 100

            # Generate ContractNo
            contract_no = f"{datetime.now().strftime('%y%m%d')}-{str(Contracts.objects.count() + 1).zfill(4)}"
            while Contracts.objects.filter(ContractNo=contract_no).exists():
                contract_no = f"{datetime.now().strftime('%y%m%d')}-{str(Contracts.objects.count() + 1).zfill(4)}"

            # Save contract
            Contracts.objects.create(
                ContractNo=contract_no,
                CreatedBy_id=customer_id,
                VehicleID=vehicle,
                InsuranceCategoryID_id=insurance_category_id,
                EstimatePremium=estimate_premium,
                DurationID=duration_id,
                MaxPersonCompensation=vehicle_type.MaxPersonalCompensation,
                MaxPropertyCompensation=vehicle_type.MaxPropertyCompensation,
                Status='Awaiting',
                CreatedAt=datetime.now()
            )
            messages.success(request, "You have successfully registered to buy insurance!")
            return redirect('contracts:contract_list')

    return render(request, 'contracts/create_civil.html', {
        'form': form,
        'durations': durations,
        'category': InsuranceCategories.objects.get(id=category_id)
    })


@customer_login_required
def create_contract_other(request, category_id):
    if not has_permission(group_id=2, function_id=4, action_id=2):
        messages.error(request, "You do not have permission to create contract.")
        return redirect("contracts:contract_list")

    customer_id = request.session['user_id']
    form = ContractForm(customer_id=customer_id)
    durations = Duration.objects.all()

    if request.method == 'POST':
        form = ContractForm(request.POST, customer_id=customer_id)
        if form.is_valid():
            vehicle = form.cleaned_data['vehicle_id']
            duration_id = form.cleaned_data['duration_id']
            insurance_category_id = form.cleaned_data['insurance_category_id']

            # Calculate Age
            current_date = datetime.now().date()
            age = relativedelta(current_date, vehicle.RegistrationDate).years
            if age > 20:
                messages.error(request, "No insurance available for this vehicle age and duration.")
                return render(request, 'contracts/create_other.html', {
                    'form': form,
                    'durations': durations,
                    'category': InsuranceCategories.objects.get(id=category_id)
                })

            # Get Depreciations Rate
            depreciation = Depreciations.objects.filter(Age=age).first()
            if not depreciation:
                messages.error(request, "No insurance available for this vehicle age and duration.")
                return render(request, 'contracts/create_other.html', {
                    'form': form,
                    'durations': durations,
                    'category': InsuranceCategories.objects.get(id=category_id)
                })

            # Get InsurancePriceList Rate
            price_list = InsurancePriceList.objects.filter(
                InsuranceCategoryID_id=insurance_category_id,
                DurationID_id=duration_id.id,
                MinAge__lte=age,
                MaxAge__gte=age
            ).first()
            if not price_list:
                messages.error(request, "No insurance available for this vehicle age and duration.")
                return render(request, 'contracts/create_other.html', {
                    'form': form,
                    'durations': durations,
                    'category': InsuranceCategories.objects.get(id=category_id)
                })

            # Calculate EstimatePremium and EstimateValue
            estimate_premium = (vehicle.PurchasePrice * (depreciation.Rate / 100) * (price_list.Rate / 100)) * 100
            estimate_value = vehicle.PurchasePrice * (depreciation.Rate / 100)

            # Generate ContractNo
            contract_no = f"{datetime.now().strftime('%y%m%d')}-{str(Contracts.objects.count() + 1).zfill(4)}"
            while Contracts.objects.filter(ContractNo=contract_no).exists():
                contract_no = f"{datetime.now().strftime('%y%m%d')}-{str(Contracts.objects.count() + 1).zfill(4)}"

            # Save contract
            Contracts.objects.create(
                ContractNo=contract_no,
                CreatedBy_id=customer_id,
                VehicleID=vehicle,
                InsuranceCategoryID_id=insurance_category_id,
                EstimateValue=estimate_value,
                EstimatePremium=estimate_premium,
                DurationID=duration_id,
                Status='Awaiting',
                CreatedAt=datetime.now()
            )
            messages.success(request, "You have successfully registered to buy insurance!")
            return redirect('contracts:contract_list')

    return render(request, 'contracts/create_other.html', {
        'form': form,
        'durations': durations,
        'category': InsuranceCategories.objects.get(id=category_id)
    })


@customer_login_required
@require_POST
def calculate_insurance(request):
    vehicle_id = request.POST.get('vehicle_id')
    category_id = request.POST.get('category_id')
    if not vehicle_id or not category_id:
        return JsonResponse({'error': 'Invalid vehicle or category'}, status=400)

    try:
        vehicle = Vehicles.objects.select_related('VehicleTypeID').get(id=vehicle_id,
                                                                       CustomerID_id=request.session['user_id'])
        category = InsuranceCategories.objects.get(id=category_id)
        durations = Duration.objects.all()
        current_date = datetime.now().date()
        age = relativedelta(current_date, vehicle.RegistrationDate).years
        data = []

        for duration in durations:
            item = {'duration_id': duration.id, 'months': float(duration.Months), 'available': True}

            if category_id == '1':  # Civil liability
                price_list = InsurancePriceList.objects.filter(
                    InsuranceCategoryID_id=category_id,
                    DurationID_id=duration.id
                ).first()
                if price_list:
                    item['estimate_premium'] = float((vehicle.VehicleTypeID.Fee * price_list.Rate) / 100)
                    item['max_person_compensation'] = float(vehicle.VehicleTypeID.MaxPersonalCompensation)
                    item['max_property_compensation'] = float(vehicle.VehicleTypeID.MaxPropertyCompensation)
                else:
                    item['available'] = False
                    item['error'] = "No insurance available for this vehicle age and duration."
            else:  # Other categories
                if age > 20:
                    item['available'] = False
                    item['error'] = "No insurance available for this vehicle age and duration."
                else:
                    depreciation = Depreciations.objects.filter(Age=age).first()
                    if not depreciation:
                        item['available'] = False
                        item['error'] = "No insurance available for this vehicle age and duration."
                    else:
                        price_list = InsurancePriceList.objects.filter(
                            InsuranceCategoryID_id=category_id,
                            DurationID_id=duration.id,
                            MinAge__lte=age,
                            MaxAge__gte=age
                        ).first()
                        if price_list:
                            item['estimate_premium'] = float(
                                (vehicle.PurchasePrice * (depreciation.Rate / 100) * (price_list.Rate / 100)) * 100)
                            item['max_estimate_property_compensation'] = float(
                                vehicle.PurchasePrice * (depreciation.Rate / 100))
                        else:
                            item['available'] = False
                            item['error'] = "No insurance available for this vehicle age and duration."

            data.append(item)

        return JsonResponse({'data': data})
    except Vehicles.DoesNotExist:
        return JsonResponse({'error': 'Vehicle not found'}, status=404)


# @customer_login_required
def contract_list(request):
    # Fetch contracts, their vehicle, and the vehicle's customer in one query
    contracts = Contracts.objects.select_related(
        'vehicle',
        'vehicle__customer',
        'insurance_category',
        'duration',
        'created_by'
    ).filter()

    # for c in contracts:
    #     print(f"contract {c.id} status: {c.status}")

    return render(request, 'contracts/list.html', {
        'segment': 'contracts',
        'contracts': contracts
    })
