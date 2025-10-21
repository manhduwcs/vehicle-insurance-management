from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from accounts.decorators import customer_login_required
from .models import Customer
from .forms import CustomerUpdateForm,CustomerForm
from app_helper.views import notify
from django.contrib.auth.hashers import check_password, make_password


def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'customer/customer_list.html', {'customers': customers})

def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    return render(request, 'customer/customer_detail.html', {'customer': customer})

def customer_create(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm()
    return render(request, 'customer/customer_form.html', {'form': form})

def customer_update(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            notify(request, "Customer information updated successfully.", "success")
            return redirect('customer_list')
        else:
            notify(request, "Update failed. Please check the form and try again.", "error")
            print(form.errors)
    else:
        
        form = CustomerForm(instance=customer)
    return render(request, 'customer/customer_update.html', {'form': form, 'customer': customer})

def customer_delete(request, pk):
    try:
        customer = get_object_or_404(Customer, pk=pk)
        if request.method == "POST":
            customer_name = str(customer)  # optional: display name in toast
            customer.delete()
            notify(request, f"Customer '{customer_name}' deleted successfully.", "success")
        else:
            notify(request, "Invalid request method. Deletion not performed.", "warning")
    except Exception as e:
        notify(request, f"Failed to delete customer. Error: {str(e)}", "error")

    return redirect('customer_list')


@customer_login_required
def customer_info(request):
    customer = request.customer
    
    if request.method == 'POST':
        form = CustomerUpdateForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Personal information updated successfully!')
            return redirect('customer_info')
        else:
           
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomerUpdateForm(instance=customer)
    print(customer)
    return render(request, 'customer/customer_info.html', {'form': form})

@customer_login_required
def change_password(request):
    if request.method == 'POST':
        try:
            customer = request.customer
            current_password = request.POST.get('current_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            
            
            if not check_password(current_password, customer.password):
                messages.error(request, 'Current password is incorrect!')
            
            elif new_password != confirm_password:
                messages.error(request, 'New passwords do not match!')
            
            elif len(new_password) < 8:
                messages.error(request, 'Password must be at least 8 characters!')
            else:
                customer.password = make_password(new_password)
                customer.save()
                messages.success(request, 'Password changed successfully!')
        except Customer.DoesNotExist:
            messages.error(request, 'Customer not found!')
        except Exception as e:
            messages.error(request, f'Error changing password: {str(e)}')
    
    return redirect('customer_info')