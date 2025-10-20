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
from categories.models import Duration, InsuranceCategories, InsurancePriceList
from contracts.models import Contracts, Depreciations
from vehicle.models import Vehicle



@customer_login_required
def list_insurance_categories(request):
    # if not has_permission(group_id=2, function_id=4, action_id=2):  # ManageContracts, Create
    #     messages.error(request, "You do not have permission to create contract.")
    #     return redirect("contracts:contract_list")

    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        vehicles = Vehicle.objects.filter(customer_id=request.session['user_id'])
        if not vehicles.exists():
            messages.error(request, "You need to register your vehicle on the system before purchasing insurance.")
            return render(request, 'categories/list.html', {'categories': InsuranceCategories.objects.all()})
        if category_id == '1':
            return redirect('contracts:create_contract_civil', category_id=category_id)
        return redirect('contracts:create_contract_other', category_id=category_id)

    return render(request, 'list_categories/list.html', {
        'categories': InsuranceCategories.objects.all()
    })


@customer_login_required
def create_contract_civil(request, category_id):
    # if not has_permission(group_id=2, function_id=4, action_id=2):
    #     messages.error(request, "You do not have permission to create contract.")
    #     return redirect("contracts:contract_list")

    customer_id = request.session['user_id']
    form = ContractForm(customer_id=customer_id)
    durations = Duration.objects.all()

    if request.method == 'POST':
        form = ContractForm(request.POST, customer_id=customer_id)
        print("Received POST data:", request.POST)  # Debug
        if form.is_valid():
            vehicle = form.cleaned_data['vehicle_id']
            duration_id = form.cleaned_data['duration_id']
            insurance_category_id = form.cleaned_data['insurance_category_id']

            # Calculate EstimatePremium
            vehicle_type = vehicle.vehicle_type
            price_list = InsurancePriceList.objects.filter(
                insurance_category_id=insurance_category_id,
                duration=duration_id
            ).first()
            if not price_list:
                messages.error(request, "No insurance available for this vehicle age and duration.")
                return render(request, 'contracts/create_civil.html', {
                    'form': form,
                    'durations': durations,
                    'category': InsuranceCategories.objects.get(id=category_id)
                })

            estimate_premium = vehicle_type.fee * (price_list.rate / 100) * (duration_id.months / 12)

            # Generate ContractNo
            contract_no = f"{datetime.now().strftime('%y%m%d')}-{str(Contracts.objects.count() + 1).zfill(4)}"
            while Contracts.objects.filter(contract_no=contract_no).exists():
                contract_no = f"{datetime.now().strftime('%y%m%d')}-{str(Contracts.objects.count() + 1).zfill(4)}"

            # Save contract
            Contracts.objects.create(
                contract_no=contract_no,
                created_by_id=customer_id,
                vehicle=vehicle,
                insurance_category_id=insurance_category_id,
                estimate_premium=estimate_premium,
                duration=duration_id,
                max_person_compensation=vehicle_type.max_personal_compensation,
                max_property_compensation=vehicle_type.max_property_compensation,
                status='Awaiting',
                created_at=datetime.now()
            )
            messages.success(request, "You have successfully registered to buy insurance!")
            return redirect('contracts:contract_list_customer')
        else:
            print("Form errors:", form.errors)

    return render(request, 'contracts/create_civil.html', {
        'form': form,
        'durations': durations,
        'category': InsuranceCategories.objects.get(id=category_id)
    })


@customer_login_required
def create_contract_other(request, category_id):
    # if not has_permission(group_id=2, function_id=4, action_id=2):
    #     messages.error(request, "You do not have permission to create contract.")
    #     return redirect("contracts:contract_list")

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
            age = relativedelta(current_date, vehicle.registration_date).years
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
                insurance_category_id=insurance_category_id,
                duration=duration_id,
                min_age__lte=age,
                max_age__gte=age
            ).first()
            if not price_list:
                messages.error(request, "No insurance available for this vehicle age and duration.")
                return render(request, 'contracts/create_other.html', {
                    'form': form,
                    'durations': durations,
                    'category': InsuranceCategories.objects.get(id=category_id)
                })

            # Calculate EstimatePremium and EstimateValue
            estimate_premium = (
                        vehicle.purchase_price * depreciation.Rate * (price_list.rate / 100) * (duration_id.months / 12))
            estimate_value = vehicle.purchase_price * depreciation.Rate * (price_list.max_coverage_rate / 100)

            # Generate ContractNo
            contract_no = f"{datetime.now().strftime('%y%m%d')}-{str(Contracts.objects.count() + 1).zfill(4)}"
            while Contracts.objects.filter(contract_no=contract_no).exists():
                contract_no = f"{datetime.now().strftime('%y%m%d')}-{str(Contracts.objects.count() + 1).zfill(4)}"

            # Save contract
            Contracts.objects.create(
                contract_no=contract_no,
                created_by_id=customer_id,
                vehicle=vehicle,
                insurance_category_id=insurance_category_id,
                estimate_value=estimate_value,
                estimate_premium=estimate_premium,
                duration=duration_id,
                status='Awaiting',
                created_at=datetime.now()
            )
            messages.success(request, "You have successfully registered to buy insurance!")
            return redirect('contracts:contract_list_customer')

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
        vehicle = Vehicle.objects.select_related('vehicle_type').get(id=vehicle_id, customer_id=request.session['user_id'])
        category = InsuranceCategories.objects.get(id=category_id)
        durations = Duration.objects.all()
        current_date = datetime.now().date()
        age = relativedelta(current_date, vehicle.registration_date).years
        data = []

        for duration in durations:
            item = {'duration_id': duration.id, 'months': float(duration.months), 'available': True}

            if int(category_id) == 1:  # Civil liability
                price_list = InsurancePriceList.objects.filter(
                    insurance_category_id=category_id,
                    duration=duration
                ).first()
                if price_list:
                    item['estimate_premium'] = float((vehicle.vehicle_type.fee * price_list.rate) / 100)
                    item['max_person_compensation'] = float(vehicle.vehicle_type.max_personal_compensation)
                    item['max_property_compensation'] = float(vehicle.vehicle_type.max_property_compensation)
                else:
                    item['available'] = False
                    item['error'] = "No insurance available for this duration."
            else:  # Other categories
                print(f"Processing category {category_id}, age {age}, duration {duration.id}")  # Debug
                if age > 20:
                    item['available'] = False
                    item['error'] = "Vehicle age exceeds 20 years."
                else:
                    depreciation = Depreciations.objects.filter(Age=age).first()
                    if not depreciation:
                        item['available'] = False
                        item['error'] = "No depreciation rate for this vehicle age."
                    else:
                        print(f"Depreciation rate: {depreciation.Rate}")  # Debug
                        price_list = InsurancePriceList.objects.filter(
                            insurance_category_id=category_id,
                            duration=duration,
                            min_age__lte=age,
                            max_age__gte=age
                        ).first()
                        if price_list:
                            print(f"Price list rate: {price_list.rate}")  # Debug
                            item['estimate_premium'] = float(
                                (vehicle.purchase_price * (depreciation.Rate) * (price_list.rate / 100) * (duration.months / 12)))
                            item['max_estimate_property_compensation'] = float(
                                vehicle.purchase_price * (depreciation.Rate) * (price_list.max_coverage_rate / 100))
                        else:
                            item['available'] = False
                            item['error'] = "No matching price list for this duration and age."

            data.append(item)

        return JsonResponse({'data': data})
    except Vehicle.DoesNotExist:
        return JsonResponse({'error': 'Vehicle not found'}, status=404)

@customer_login_required
def contract_list_customer(request):
    # Fetch contracts for the current customer
    customer_id = request.session['user_id']
    contracts = Contracts.objects.select_related(
        'vehicle',
        'vehicle__customer',
        'insurance_category',
        'duration',
        'created_by'
    ).filter(created_by_id=customer_id)

    return render(request, 'contracts/list_customer.html', {
        'segment': 'contracts',
        'contracts': contracts
    })
