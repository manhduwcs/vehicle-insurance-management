from django.shortcuts import render, get_object_or_404, redirect
from contracts.forms import ContractUpdateForm
from contracts.models import ContractStatus, Contracts
from accounts.decorators import employee_login_required
from django.contrib import messages
from app_helper.views import notify
from vehicle.models import Vehicle
from django.utils import timezone


from pathlib import Path


# @customer_login_required
def contract_list(request):
    # if not has_permission(group_id=2, function_id=4, action_id=2):  # ManageContracts, Create
    #     messages.error(request, "You do not have permission to create contract.")
    #     return redirect("contracts:contract_list")

    contracts = Contracts.objects.select_related(
        'vehicle',
        'vehicle__customer',
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

    context = {
        'segment': 'contracts',
        'contract': contract,
        'vehicle': contract.vehicle,
        'customer': contract.vehicle.customer,
        'insurance_category': contract.insurance_category,
        'duration': contract.duration,
    }
    return render(request, 'contracts/customer/detail.html', context)

# @employee_login_required
def contract_update(request, pk):
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
