from datetime import datetime
from decimal import Decimal

from dateutil.relativedelta import relativedelta
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from accounts.decorators import customer_login_required, employee_login_required
from categories.models import Duration, InsuranceCategories, InsurancePriceList
from contracts.forms import ContractForm, ContractUpdateForm
from contracts.models import ContractStatus, Contracts, Depreciations
from permissions.views import has_permission
from vehicles.models import Vehicles
from vehicle_types.models import VehicleTypes
from app_helper.views import notify
from customer.models import Customer
from permissions.constants import FunctionIds, ActionIds

from pathlib import Path


# @customer_login_required
def contract_list(request):
    if "username" not in request.session:
        return redirect("accounts:login")
    group_id = request.session.get("group_id")
    if not group_id or not has_permission(group_id, FunctionIds.ManageContractsByCustomers, ActionIds.View):
        messages.error(request, "You do not have permission to view the contracts.")
        return redirect("contracts_customer:contract_list")

    contracts = Contracts.objects.select_related(
        'vehicle',
        'vehicle__customer_id',
        'insurance_category',
        'duration',
        'created_by'
    ).order_by('-id')

    return render(request, 'contracts/customer/list.html', {
        'segment': 'contracts',
        'contracts': contracts
    })

# @employee_login_required
def contract_detail(request, pk):
    if "username" not in request.session:
        return redirect("accounts:login")
    group_id = request.session.get("group_id")
    if not group_id or not has_permission(group_id, FunctionIds.ManageContractsByCustomers, ActionIds.View):
        messages.error(request, "You do not have permission to view the contracts.")
        return redirect("contracts_customer:contract_list")
    contract = get_object_or_404(
        Contracts.objects.select_related(
            'vehicle',
            'vehicle__customer',
            'insurance_category',
            'duration',
            'created_by'
        ),
        pk=pk
    )

    can_edit = group_id and has_permission(group_id, FunctionIds.ManageContractsByCustomers, ActionIds.Edit)

    context = {
        'segment': 'contracts',
        'contract': contract,
        'vehicle': contract.vehicle,
        'customer': contract.vehicle.customer,
        'insurance_category': contract.insurance_category,
        'duration': contract.duration,
        'can_edit': can_edit,
    }
    return render(request, 'contracts/customer/detail.html', context)

# @employee_login_required
def contract_update(request, pk):
    if "username" not in request.session:
        return redirect("accounts:login")
    group_id = request.session.get("group_id")
    if not group_id or not has_permission(group_id, FunctionIds.ManageContractsByCustomers, ActionIds.Edit):
        messages.error(request, "You do not have permission to update the contracts.")
        return redirect("contracts_customer:contract_list")
    contract = get_object_or_404(
        Contracts.objects.select_related(
            'vehicle__customer',
            'insurance_category',
            'duration',
        ),
        pk=pk
    )

    # This must be set before calling form.is_valid() 
    current_status = contract.status
    # if request.method == "GET":
    #     form = ContractUpdateForm(instance=contract)  # binds current contract
    #     form.fields['status'].initial = current_status  # enforce default
    #     return

    if request.method == 'POST':
        form = ContractUpdateForm(request.POST, instance=contract)
        if form.is_valid():
            new_status = form.cleaned_data["status"]
            if ContractStatus.can_transition(current=current_status, new=new_status):
                print(f"can transition: {current_status}")
                contract.status = new_status
            else:
                messages.error(request, "This contract status transition is invalid !")
                return render(request, 'contracts/update.html', {
                    'form': form,        
                    'contract': contract,
                    'segment': 'contracts'
                })

            contract.deductible_value = form.cleaned_data['deductible_value']
            contract.deductible_addon = form.cleaned_data['deductible_addon']
            contract.actual_value = form.cleaned_data['actual_value']
            contract.actual_premium = form.cleaned_data['actual_premium']
            contract.note = form.cleaned_data['note']
                
            contract.save(update_fields=[
                'deductible_value',
                'deductible_addon',
                'actual_value',
                'actual_premium',
                'status',
                'note',
                'updated_at',
            ])
            notify(request, "Contract updated successfully!", "success")
            return redirect('contracts_customer:contract_detail', pk=contract.pk)
        else:
            notify(request, "Please correct the errors before updating the contract.", "error")
    else:
        form = ContractUpdateForm(instance=contract)

    context = {
        'segment': 'contracts',
        'contract': contract,
        'form': form,
    }
    return render(request, 'contracts/customer/update.html', context)

def goto_payment_choice(request, pk):
    contract = get_object_or_404(
        Contracts.objects.select_related(
            'vehicle__customer',
            'insurance_category',
            'duration',
        ),
        pk=pk
    )
    context = {
            'segment': 'contracts',
            'contract': contract
            }
    return render(request, "contracts/customer/payment_choices.html", context)
 

def payment_detail(request, pk):
    contract = get_object_or_404(
        Contracts.objects.select_related('vehicle__customer'),
        pk=pk
    )

    context = {
        "segment": "contracts",
        "contract": contract,
    }
    return render(request, "contracts/customer/payment_detail.html", context)
 

def pay_with_card(request, pk):
    contract = get_object_or_404(
        Contracts.objects.select_related(
            'vehicle__customer',
            'insurance_category',
            'duration',
        ),
        pk=pk
    )

    if request.method == "POST":
        contract.payment_type = "card"
        contract.payment_amount = contract.actual_premium or 0
        contract.payment_at = timezone.now()
        contract.status = ContractStatus.ACTIVED
        contract.save(update_fields=["payment_type", "payment_amount", "payment_at", "status"])
        print(f"contract.status = {contract.status}")
        return redirect("contracts_customer:contract_detail", pk=contract.pk)

    context = {
        "segment": "contracts",
        "contract": contract,
    }
    return render(request, "contracts/customer/payment_card.html", context)


def pay_direct(request, pk):
    contract = get_object_or_404(
        Contracts.objects.select_related(
            'vehicle__customer',
            'insurance_category',
            'duration',
        ),
        pk=pk
    )
    context = {
            'segment': 'contracts',
            'contract': contract
            }
    return render(request, "contracts/customer/payment_direct.html", context)

# @employee_login_required
def pay_with_qr(request, pk):
    contract = get_object_or_404(
        Contracts.objects.select_related(
            'vehicle__customer',
            'insurance_category',
            'duration',
        ),
        pk=pk
    )

    bank_code = "techcombank"
    bank_name = "Techcombank"
    account_number = "19038555085018"
    receiver_name = "NGUYEN DUC MANH"

    amount = contract.actual_premium
    message = f"Payment for Contract {contract.contract_no}"

    # qr_url = (
    #     f"https://img.vietqr.io/image/{bank_code}-{account_number}-compact.png"
    #     f"?amount={amount}&addInfo={message}"
    # )

    # print(f"qr_url: {qr_url}")
    qr_url = ""

    context = {
        "contract": contract,
        "segment": "contracts",
        "sub_segment": "payment",
        "bank_code": bank_code.upper(),
        "bank_name": bank_name,
        "account_number": account_number,
        "receiver_name": receiver_name,
        "amount": f"{amount:,} VND",
        "message": message,
        "qr_url": qr_url,
    }
    return render(request, "contracts/customer/payment_qr.html", context)


# @customer_login_required
def list_insurance_categories(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        vehicles = Vehicles.objects.filter(customer_id=request.session['user_id'])
        if not vehicles.exists():
            messages.warning(request, "You need to register your vehicle on the system before purchasing insurance.")
            return render(request, 'categories/list.html', {'categories': InsuranceCategories.objects.all()})

        # Validate personal information
        customer = Customer.objects.get(id=request.session['user_id'])
        required_fields = [
            customer.identify_number,
            customer.identify_address,
            customer.identify_date,
            customer.issuing_authority
        ]
        if any(field is None or field == '' for field in required_fields):
            return JsonResponse({
                'success': False,
                'message': 'You need to provide personal information before purchasing insurance.'
            })

        if category_id == '1':
            return redirect('contracts_customer:create_contract_civil', category_id=category_id)
        return redirect('contracts_customer:create_contract_other', category_id=category_id)

    return render(request, 'contracts/customer/list_category.html', {
        'categories': InsuranceCategories.objects.all()
    })


# @customer_login_required
def create_contract_civil(request, category_id):
    if "username" not in request.session:
        return redirect("accounts:login")
    group_id = request.session.get("group_id")
    if not group_id or not has_permission(group_id, FunctionIds.ManageContractsByCustomers, ActionIds.Create):
        messages.error(request, "You do not have permission to create the contracts.")
        return redirect("contracts_customer:contract_list")

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
                return render(request, 'contracts/customer/create_civil.html', {
                    'form': form,
                    'durations': durations,
                    'category': InsuranceCategories.objects.get(id=category_id)
                })

            rate_percentage = Decimal(str(price_list.rate)) / Decimal('100')
            duration_factor = Decimal(str(duration_id.months)) / Decimal('12')
            estimate_premium = vehicle_type.fee * rate_percentage * duration_factor

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
            return redirect('contracts_customer:contract_list')
        else:
            print("Form errors:", form.errors)

    return render(request, 'contracts/customer/create_civil.html', {
        'form': form,
        'durations': durations,
        'category': InsuranceCategories.objects.get(id=category_id)
    })


# @customer_login_required
def create_contract_other(request, category_id):
    if "username" not in request.session:
        return redirect("accounts:login")
    group_id = request.session.get("group_id")
    if not group_id or not has_permission(group_id, FunctionIds.ManageContractsByCustomers, ActionIds.Create):
        messages.error(request, "You do not have permission to create the contracts.")
        return redirect("contracts_customer:contract_list")

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
                return render(request, 'contracts/customer/create_other.html', {
                    'form': form,
                    'durations': durations,
                    'category': InsuranceCategories.objects.get(id=category_id)
                })

            # Calculate EstimatePremium and EstimateValue
            rate_percentage = Decimal(str(price_list.rate)) / Decimal('100')
            max_coverage_percentage = Decimal(str(price_list.max_coverage_rate)) / Decimal('100')
            duration_factor = Decimal(str(duration_id.months)) / Decimal('12')
            estimate_premium = (
                    vehicle.purchase_price * Decimal(str(depreciation.Rate)) * rate_percentage * duration_factor
            )
            estimate_value = vehicle.purchase_price * Decimal(str(depreciation.Rate)) * max_coverage_percentage

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
            return redirect('contracts_customer:contract_list')

    return render(request, 'contracts/customer/create_other.html', {
        'form': form,
        'durations': durations,
        'category': InsuranceCategories.objects.get(id=category_id)
    })


# @customer_login_required
@require_POST
def calculate_insurance(request):
    vehicle_id = request.POST.get('vehicle_id')
    category_id = request.POST.get('category_id')
    if not vehicle_id or not category_id:
        return JsonResponse({'error': 'Invalid vehicle or category'}, status=400)

    try:
        vehicle = Vehicles.objects.select_related('vehicle_type').get(id=vehicle_id, customer_id=request.session['user_id'])
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
                    item['estimate_premium'] = float((vehicle.vehicle_type.fee * price_list.rate) / 100 * duration.months / 12)
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
                            rate_percentage = Decimal(str(price_list.rate)) / Decimal('100')
                            max_coverage_percentage = Decimal(str(price_list.max_coverage_rate)) / Decimal('100')
                            duration_factor = Decimal(str(duration.months)) / Decimal('12')
                            item['estimate_premium'] = float(
                                vehicle.purchase_price * Decimal(
                                    str(depreciation.Rate)) * rate_percentage * duration_factor
                            )
                            item['max_estimate_property_compensation'] = float(
                                vehicle.purchase_price * Decimal(str(depreciation.Rate)) * max_coverage_percentage
                            )
                        else:
                            item['available'] = False
                            item['error'] = "No matching price list for this duration and age."

            data.append(item)

        return JsonResponse({'data': data})
    except Vehicles.DoesNotExist:
        return JsonResponse({'error': 'Vehicle not found'}, status=404)

# @customer_login_required
# def contract_list_customer(request):
#     if "username" not in request.session:
#         return redirect("accounts:login")
#     group_id = request.session.get("group_id")
#     if not group_id or not has_permission(group_id, FunctionIds.ManageContracts, ActionIds.View):
#         messages.error(request, "You do not have permission to view the contracts.")
#         return redirect("customer:customer_info")
#
#     customer_id = request.session['user_id']
#     contracts = Contracts.objects.select_related(
#         'vehicle',
#         'vehicle__customer',
#         'insurance_category',
#         'duration',
#         'created_by'
#     ).filter(created_by_id=customer_id)
#
#     return render(request, 'contracts/customer/list_customer.html', {
#         'segment': 'contracts',
#         'contracts': contracts
#     })
