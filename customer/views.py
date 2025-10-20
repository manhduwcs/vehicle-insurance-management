from django.shortcuts import render, get_object_or_404, redirect
from .models import Customer
from .forms import CustomerForm
from app_helper.views import notify

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