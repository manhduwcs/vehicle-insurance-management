import uuid
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django import forms
from .models import Claim
from vehicles.models import Vehicles
from contracts.models import Contracts
from .forms import ClaimForm, ClaimApprovalForm
from django.contrib import messages
from django.core.paginator import Paginator


from django.db.models import Max

def generate_claim_no():
    
    last_claim = Claim.objects.aggregate(last_no=Max('claim_no'))['last_no']
    if not last_claim:
        return "CLM0001"
    try:
        number = int(last_claim.replace("CLM", ""))
        return f"CLM{number + 1:04d}"
    except ValueError:
        
        return f"CLM-{uuid.uuid4().hex[:6].upper()}"



def claim_list(request):
    claims = Claim.objects.filter(customer=request.user).order_by('-id')
    return render(request, "claims/list.html", {"claims": claims, "segment": "claim"})


def claim_create(request):
    if request.method == "POST":
        form = ClaimForm(request.POST)
        if form.is_valid():
            claim = form.save(commit=False)

          
            contract = form.cleaned_data.get("contract")
            claim.vehicles = contract.vehicle

            claim.customer = request.user
            claim.claim_no = generate_claim_no()
            claim.status = "Pending"
            print(claim.vehicles)
            
         

            claim.save()
            return redirect("claim_list")
        else:
            print("Form errors:", form.errors)
    else:
        form = ClaimForm()
        contracts = Contracts.objects.filter(
            created_by=request.user,
            status__iexact="Actived"  
        )
        form.fields['contract'].queryset = contracts
        # Hide vehicle field initially, it will be auto-populated
        #form.fields['vehicle'].widget = forms.HiddenInput()
    return render(request, "claims/create.html", {"form": form, "segment": "claim"})


def claim_detail_customer(request, pk):
    """Display claim detail and handle status updates"""
    claim = get_object_or_404(Claim, pk=pk)
    
    context = {
        'claim': claim,
    }
    return render(request, 'claims/detail.html', context)


def claim_update_status(request, pk, action):
    """Handle claim status updates (accept/reject by customer)"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    
    claim = get_object_or_404(Claim, pk=pk)
    
    
    # Check if claim is in approved status
    if claim.status != 'Approved':
        return JsonResponse({
            'success': False, 
            'message': f'Cannot modify claim with status: {claim.status}'
        })
    
    # Update status based on action
    if action == 'accept':
        claim.status = 'Completed'
        message = 'Claim has been accepted and marked as completed.'
    elif action == 'reject':
        claim.status = 'Rejected'
        message = 'Claim has been rejected.'
    else:
        return JsonResponse({'success': False, 'message': 'Invalid action'})
    
    claim.save()
    
    return JsonResponse({
        'success': True, 
        'message': message,
        'new_status': claim.status
    })

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


def claims_list_admin(request):
    """
    Display list of all claims with basic information
    """
    claims = Claim.objects.select_related('customer', 'vehicles', 'contract').all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        claims = claims.filter(
            claim_no__icontains=search_query
        ) | claims.filter(
            customer__name__icontains=search_query
        )
    
    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        claims = claims.filter(status=status_filter)
    
    # Pagination
    paginator = Paginator(claims, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'status_choices': ['Pending', 'Approved', 'Completed', 'Rejected'],
        'segment': 'claim',
    }

    return render(request, 'claims/claims_list_admin.html', context)

def claim_detail_admin(request, pk):
    """
    Display detailed information of a specific claim
    """
    claim = get_object_or_404(
        Claim.objects.select_related('customer', 'vehicles', 'contract'),
        id=pk
    )
    
    # Check if user can update the claim (only Pending claims)
    can_update = claim.status == 'Pending'
    
    context = {
        'claim': claim,
        'can_update': can_update,
        'segment': 'claim',
    }

    return render(request, 'claims/claim_detail_admin.html', context)


def claim_approve(request, pk):
    """
    Update claim with compensation details and change status to Approved
    """
    claim = get_object_or_404(Claim, id=pk)
    
    # Only allow updates for Pending claims
    if claim.status != 'Pending':
        messages.error(request, 'Only Pending claims can be updated.')
        return redirect('claim_detail', claim_id=claim.id)
    
    if request.method == 'POST':
        form = ClaimApprovalForm(request.POST, instance=claim)
        if form.is_valid():
            claim = form.save(commit=False)
            claim.status = 'Approved'
            claim.save()
            messages.success(request, f'Claim #{claim.claim_no} has been verified and approved.')
            return redirect('claim_detail_admin', claim_id=claim.id)
    else:
        form = ClaimApprovalForm(instance=claim)
    
    context = {
        'form': form,
        'claim': claim,
        'segment': 'claim',
    }
    
    return render(request, 'claims/claim_approve.html', context)
