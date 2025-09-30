from django.shortcuts import render, get_object_or_404, redirect
from .models import Discount
from .forms import DiscountForm

# List
def discount_list(request):
    discounts = Discount.objects.all().order_by('-id')
    context = {
        "discounts": discounts,
        "segment": "discount",
    }
    return render(request, "discount/list.html", context)

# Detail
def discount_detail(request, pk):
    discount = get_object_or_404(Discount, pk=pk)
    context = {
        "discount": discount,
        "segment": "discount",
    }
    return render(request, "discount/detail.html", context)

# Create
def discount_create(request):
    if request.method == "POST":
        form = DiscountForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("discount_list")
    else:
        form = DiscountForm()
    context = {
        "form": form,
        "segment": "discount",
    }
    return render(request, "discount/create.html", context)

# Update
def discount_update(request, pk):
    discount = get_object_or_404(Discount, pk=pk)
    if request.method == "POST":
        form = DiscountForm(request.POST, instance=discount)
        if form.is_valid():
            form.save()
            return redirect("discount_list")
    else:
        form = DiscountForm(instance=discount)
    context = {
        "discount": discount,
        "form": form,
        "segment": "discount",
    }
    return render(request, "discount/update.html", context)

# Delete
def discount_delete(request, pk):
    discount = get_object_or_404(Discount, pk=pk)
    if request.method == "POST":
        discount.delete()
        return redirect("discount_list")
    return redirect("discount_list")