# insurance_category/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import InsuranceCategory
from .forms import InsuranceCategoryForm  

# List
def insurance_category_list(request):
    categories = InsuranceCategory.objects.all().order_by('-id')
    context = {
        "categories": categories,
        "segment": "insurance_category",
    }
    return render(request, "insurance_category/list.html", context)

# Detail
def insurance_category_detail(request, pk):
    category = get_object_or_404(InsuranceCategory, pk=pk)
    context = {
        "category": category,
        "segment": "insurance_category",
    }
    return render(request, "insurance_category/detail.html", context)

# Create
def insurance_category_create(request):
    if request.method == "POST":
        form = InsuranceCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("insurance_category_list")
    else:
        form = InsuranceCategoryForm()
    return redirect("insurance_category_list")

# Update
def insurance_category_update(request, pk):
    category = get_object_or_404(InsuranceCategory, pk=pk)
    print(f"category update : {category.id}, {category.name}, {category.description}")
    if request.method == "POST":
        form = InsuranceCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect("insurance_category_list")
    else:
        form = InsuranceCategoryForm(instance=category)
    context = {
        "category": category,
        "segment": "insurance_category",
        "form": form
    }
    return render(request, "insurance_category/update.html", context)

# Delete
def insurance_category_delete(request, pk):
    category = get_object_or_404(InsuranceCategory, pk=pk)
    if request.method == "POST":
        category.delete()
        return redirect("insurance_category_list")
    return redirect("insurance_category_list")