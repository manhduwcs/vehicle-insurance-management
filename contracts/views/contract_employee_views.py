from django.shortcuts import render, redirect
from django.contrib import messages
from contracts.forms import ContractUpdateForm
from contracts.models import ContractStatus
from app_helper.views import notify

from contracts.models import Contracts, Depreciations
from vehicle_types.models import VehicleTypes
from decimal import Decimal
from django.shortcuts import get_object_or_404, redirect, render
# from accounts.decorators import employee_login_required

# @employee_login_required
def contract_list(request):
    # if not has_permission(group_id=2, function_id=4, action_id=2):  # ManageContracts, Create
    #     messages.error(request, "You do not have permission to create contract.")
    #     return redirect("contracts_customer:contract_list")

    contracts = Contracts.objects.select_related(
        'vehicle',
        'vehicle__customer_id',
        'insurance_category',
        'duration',
        'created_by'
    ).order_by('-id')

    return render(request, 'contracts/employee/list.html', {
        'segment': 'contracts',
        'contracts': contracts
    })

# @employee_login_required
def contract_detail(request, pk):
    contract = get_object_or_404(
        Contracts.objects.select_related(
            'vehicle',
            'vehicle__customer_id',
            'insurance_category',
            'duration',
            'created_by'
        ),
        pk=pk
    )

    context = {
        'segment': 'contracts',
        'contract': contract,
        'vehicle': contract.vehicle,
        'customer': contract.vehicle.customer_id,
        'insurance_category': contract.insurance_category,
        'duration': contract.duration,
    }
    return render(request, 'contracts/employee/detail.html', context)

# @employee_login_required
def contract_update(request, pk):
    contract = get_object_or_404(
        Contracts.objects.select_related(
            'vehicle__customer_id',
            'insurance_category',
            'duration',
        ),
        pk=pk
    )

    # This must be set before calling form.is_valid() 
    current_status = contract.status

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
            return render(request, 'contracts/employee/detail.html', { 'contract': contract, 'segment': 'contracts' })
        else:
            notify(request, "Please correct the errors before updating the contract.", "error")
            return render(request, 'contracts/employee/update.html', {
                'form': form,
                'contract': contract
            })
    else:
        form = ContractUpdateForm(instance=contract)

    context = {
        'segment': 'contracts',
        'contract': contract,
        'form': form,
    }
    return render(request, 'contracts/employee/update.html', context)

def contract_reject(request, pk):
    contract = get_object_or_404(
        Contracts.objects.select_related(
            'vehicle',
            'vehicle__customer_id',
            'insurance_category',
            'duration',
            'created_by'
        ),
        pk=pk
    )

    if request.method == 'POST':
        contract.status = ContractStatus.REJECTED
        contract.save()
        notify(request, f"Contract {contract.contract_no} has been rejected successfully.")
        context = {
            "segment": "contracts",
            "contract": contract,
        }
        return render(request, "contracts/employee/detail.html", context)

    return redirect('contracts_employee:contracts_detail', pk=contract.pk)

def payment_detail(request, pk):
    contract = get_object_or_404(
        Contracts.objects.select_related('vehicle__customer_id'),
        pk=pk
    )

    context = {
        "segment": "contracts",
        "contract": contract,
    }
    return render(request, "contracts/employee/payment_detail.html", context)
