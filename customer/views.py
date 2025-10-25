from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Customer
from .forms import CustomerUpdateForm,CustomerForm
from app_helper.views import notify
from django.contrib.auth.hashers import check_password, make_password
from permissions.constants import FunctionIds, ActionIds
from permissions.views import has_permission


def customer_list(request):
    if "username" not in request.session:
        return redirect("employee:login")
    group_id = request.session.get("group_id", None)
    if not has_permission(group_id, FunctionIds.ManageCustomersByEmployees, ActionIds.View):
        messages.error(request, "You do not have permission to view the customers list.")
        return redirect("home")
    customers = Customer.objects.all()
    return render(request, 'customer/customer_list.html', {'customers': customers})

def customer_detail(request, pk):
    if "username" not in request.session:
        return redirect("employee:login")
    group_id = request.session.get("group_id", None)
    if not has_permission(group_id, FunctionIds.ManageCustomersByEmployees, ActionIds.View):
        messages.error(request, "You do not have permission to view the customers detail.")
        return redirect("customer:customer_list")
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
    if "username" not in request.session:
        return redirect("accounts:login")
    group_id = request.session.get("group_id", None)
    if not has_permission(group_id, FunctionIds.ManageCustomersByCustomers, ActionIds.Edit):
        messages.error(request, "You do not have permission to update customer's detail.")
        return redirect("customer:customer_info")
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            notify(request, "Customer information updated successfully.", "success")
            return redirect('customer:customer_info')
        else:
            notify(request, "Update failed. Please check the form and try again.", "error")
            print(form.errors)
    else:
        
        form = CustomerForm(instance=customer)
    return render(request, 'customer/customer_update.html', {'form': form, 'customer': customer})

def customer_delete(request, pk):
    if "username" not in request.session:
        return redirect("employee:login")
    group_id = request.session.get("group_id", None)
    if not has_permission(group_id, FunctionIds.ManageCustomersByEmployees, ActionIds.Delete):
        messages.error(request, "You do not have permission to remove customer.")
        return redirect("home")
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



def customer_info(request):
    if "username" not in request.session:
        return redirect("accounts:login")
    group_id = request.session.get("group_id")
    if not group_id or not has_permission(group_id, FunctionIds.ManageCustomersByCustomers, ActionIds.View):
        messages.error(request, "You do not have permission to view the customer information.")
        return redirect("accounts:login")

    customer = request.user
    if request.method == 'POST':
        form = CustomerUpdateForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Personal information updated successfully!')
            return redirect('customer:customer_info')
        else:
           
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomerUpdateForm(instance=customer)
    return render(request, 'customer/customer_info.html', {'form': form, 'customer': customer})


def change_password(request):
    if "username" not in request.session:
        return redirect("accounts:login")
    group_id = request.session.get("group_id")
    if not group_id or not has_permission(2, FunctionIds.ManageCustomersByCustomers, ActionIds.Edit):
        messages.error(request, "You do not have permission to change the password.")
        return redirect("customer:customer_info")

    if request.method == 'POST':
        try:
            customer = request.user
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
