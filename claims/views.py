from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django import forms
from .models import Claim
from vehicles.models import Vehicles
from contracts.models import Contracts
from .forms import ClaimForm


def claim_list(request):
    # Chỉ hiển thị claims của customer đang đăng nhập
    claims = Claim.objects.filter(customer=request.user).order_by('-id')
    return render(request, "claims/list.html", {"claims": claims, "segment": "claim"})


def claim_create(request):
    if request.method == "POST":
        form = ClaimForm(request.POST)
        if form.is_valid():
            claim = form.save(commit=False)
            # Tự động gán customer từ session
            claim.customer = request.user
            claim.status = 'Pending'
            claim.save()
            return redirect("claim_list")
        else:
            # If form is not valid, show errors
            print("Form errors:", form.errors)
    else:
        form = ClaimForm()
        # Chỉ hiển thị contracts của customer đang đăng nhập
        contracts = Contracts.objects.filter(created_by=request.user).select_related('vehicle')
        form.fields['contract'].queryset = contracts
        # Hide vehicle field initially, it will be auto-populated
        form.fields['vehicle'].widget = forms.HiddenInput()
    return render(request, "claims/create.html", {"form": form, "segment": "claim"})


def claim_detail(request, pk):
    # Chỉ cho phép xem claim của chính customer đó
    claim = get_object_or_404(Claim, pk=pk, customer=request.user)
    return render(request, "claims/detail.html", {"claim": claim, "segment": "claim"})


def claim_update(request, pk):
    # Chỉ cho phép sửa claim của chính customer đó
    claim = get_object_or_404(Claim, pk=pk, customer=request.user)
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
    AJAX: return list of contracts for a given vehicle id (chỉ của customer đang đăng nhập)
    """
    qs = Contracts.objects.filter(vehicle_id=vehicle_id, created_by=request.user)
    data = [{"id": c.id, "contract_no": getattr(c, "contract_no", str(c.id))} for c in qs]
    return JsonResponse({"contracts": data})


def vehicle_for_contract(request, contract_id):
    """
    AJAX: return vehicle information for a given contract id (chỉ của customer đang đăng nhập)
    """
    try:
        contract = Contracts.objects.select_related('vehicle', 'vehicle__vehicle_type').filter(created_by=request.user).get(id=contract_id)
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
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
