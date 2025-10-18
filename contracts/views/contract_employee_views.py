from django.shortcuts import render, get_object_or_404, redirect
from contracts.forms import ContractUpdateForm
from contracts.models import Contracts
from accounts.decorators import employee_login_required
from django.contrib import messages


# @employee_login_required
def contract_detail(request, pk):
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
        'contract': contract,
        'vehicle': contract.vehicle,
        'customer': contract.vehicle.customer,
        'insurance_category': contract.insurance_category,
        'duration': contract.duration,
    }
    return render(request, 'contracts/detail.html', context)

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

    if request.method == 'POST':
        form = ContractUpdateForm(request.POST, instance=contract)
        if form.is_valid():
            contract.save(update_fields=[
                'deductible_value',
                'deductible_addon',
                'actual_value',
                'actual_premium',
                'status',
                'note',
                'updated_at',
            ])
            messages.success(request, "Contract updated successfully.")
            return redirect('contracts:contract_detail', pk=contract.pk)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ContractUpdateForm(instance=contract)

    context = {
        'segment': 'contracts',
        'contract': contract,
        'form': form,
    }
    return render(request, 'contracts/update.html', context)
