# insurance_category/views.py
from django.contrib import messages
from permissions.views import has_permission
from django.shortcuts import render, get_object_or_404, redirect
from .models import InsuranceCategory
from .forms import InsuranceCategoryForm
from permissions.constants import FunctionIds, ActionIds


# List
def insurance_category_list(request):
    categories = InsuranceCategory.objects.all().order_by("-id")
    if "username" not in request.session:
        return redirect("employee:login")
    group_id = request.session.get("group_id", None)
    if not has_permission(group_id, FunctionIds.ManageEmployees, ActionIds.View):
        messages.error(request, "You do not have permission to view the employee list.")
        return redirect("employee:employee_list")
    context = {
        "categories": categories,
        "segment": "insurance_category",
        "can_add": has_permission(
            group_id, FunctionIds.ManageEmployees, ActionIds.Create
        ),
        "can_edit": has_permission(
            group_id, FunctionIds.ManageEmployees, ActionIds.Edit
        ),
        "can_delete": has_permission(
            group_id, FunctionIds.ManageEmployees, ActionIds.Delete
        ),
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
            return redirect("insurance_category:insurance_category_list")
    else:
        form = InsuranceCategoryForm()
    return render(request, "insurance_category/create.html", {
        "segment": "insurance_category",
        "form": form
    })


# Update
def insurance_category_update(request, pk):
    category = get_object_or_404(InsuranceCategory, pk=pk)
    print(f"category update : {category.id}, {category.name}, {category.description}")
    if request.method == "POST":
        form = InsuranceCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect("insurance_category:insurance_category_list")
    else:
        form = InsuranceCategoryForm(instance=category)
    context = {"category": category, "segment": "insurance_category", "form": form}
    return render(request, "insurance_category/update.html", context)


# Delete
def insurance_category_delete(request, pk):
    category = get_object_or_404(InsuranceCategory, pk=pk)
    if request.method == "POST":
        category.delete()
        return redirect("insurance_category:insurance_category_list")
    return redirect("insurance_category:insurance_category_list")

