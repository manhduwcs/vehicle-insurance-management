from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django import forms
from .models import Claim
from vehicles.models import Vehicles
from contracts.models import Contracts
from .forms import ClaimForm


def claim_list(request):
    if request.user.is_staff:
        claims = Claim.objects.all().order_by('-id')
    else:
        # assume User -> Customer relation exists as request.user.customer
        claims = Claim.objects.filter(customer=getattr(request.user, "customer", None)).order_by('-id')
    return render(request, "claims/list.html", {"claims": claims, "segment": "claim"})


def claim_create(request):
    if request.method == "POST":
        form = ClaimForm(request.POST)
        if form.is_valid():
            claim = form.save(commit=False)
            claim.customer = getattr(request.user, "customer", None)
            claim.status = 'Pending'
            claim.save()
            return redirect("claim_list")
    else:
        form = ClaimForm()
        # Show only contracts of current customer, vehicle will be auto-selected
        try:
            customer = getattr(request.user, "customer", None)
            if customer:
                # Get all contracts for this customer
                form.fields['contract'].queryset = Contracts.objects.filter(created_by=customer)
                # Hide vehicle field initially, it will be auto-populated
                form.fields['vehicle'].widget = forms.HiddenInput()
        except Exception:
            pass
    return render(request, "claims/create.html", {"form": form, "segment": "claim"})


def claim_detail(request, pk):
    claim = get_object_or_404(Claim, pk=pk)
    # permission: staff can view all; customers only their own
    if not request.user.is_staff and claim.customer != getattr(request.user, "customer", None):
        return redirect("claim_list")
    return render(request, "claims/detail.html", {"claim": claim, "segment": "claim"})


def claim_update(request, pk):
    claim = get_object_or_404(Claim, pk=pk)
    # only staff can update / assess
    if not request.user.is_staff:
        return redirect("claim_list")
    if request.method == "POST":
        form = ClaimForm(request.POST, instance=claim)
        if form.is_valid():
            form.save()
            return redirect("claim_detail", pk=claim.pk)
    else:
        form = ClaimForm(instance=claim)
    return render(request, "claims/update.html", {"form": form, "claim": claim, "segment": "claim"})


def contracts_for_vehicle(request, vehicle_id):
    """
    AJAX: return list of contracts for a given vehicle id
    """
    qs = Contracts.objects.filter(vehicle_id=vehicle_id)
    data = [{"id": c.id, "contract_no": getattr(c, "contract_no", str(c.id))} for c in qs]
    return JsonResponse({"contracts": data})


def vehicle_for_contract(request, contract_id):
    """
    AJAX: return vehicle information for a given contract id
    """
    try:
        contract = Contracts.objects.select_related('vehicle').get(id=contract_id)
        vehicle = contract.vehicle
        data = {
            "id": vehicle.id,
            "name": vehicle.name,
            "model": vehicle.model,
            "number": vehicle.number,
            "vehicle_type": vehicle.vehicle_type.name if vehicle.vehicle_type else "Unknown"
        }
        return JsonResponse({"vehicle": data})
    except Contracts.DoesNotExist:
        return JsonResponse({"error": "Contract not found"}, status=404)
