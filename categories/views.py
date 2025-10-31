from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.forms import modelformset_factory
from django.db import transaction
from .models import InsuranceCategories, Duration, InsurancePriceList
from .forms import InsuranceCategoryForm, InsurancePriceListForm
from employee.views import has_permission
from permissions.constants import FunctionIds, ActionIds
from decimal import Decimal, InvalidOperation

def category_list(request):
    if 'username' not in request.session:
        return redirect('employee:login')
    user_group_id = request.session.get('group_id', None)
    if not has_permission(user_group_id, FunctionIds.ManageInsuranceCategories, ActionIds.View):
        messages.error(request, "You do not have permission to view insurance categories.")
        return redirect('home')

    categories = InsuranceCategories.objects.all()
    durations = Duration.objects.all()
    price_lists = InsurancePriceList.objects.select_related('insurance_category', 'duration').all()
    # Get a list of unique (MinAge, MaxAge) pairs, sort by MinAge
    age_ranges = InsurancePriceList.objects.values('min_age', 'max_age').distinct().order_by('min_age')

    category_max_coverage = {}
    for category in categories:
        first_price = InsurancePriceList.objects.filter(insurance_category=category).first()  # Query trực tiếp
        category_max_coverage[category.id] = first_price.max_coverage_rate if first_price else 0

    return render(request, 'categories/list.html', {
        'categories': categories,
        'durations': durations,
        'price_lists': price_lists,
        'age_ranges': age_ranges,
        'category_max_coverage': category_max_coverage,
        'can_add': has_permission(user_group_id, FunctionIds.ManageInsuranceCategories, ActionIds.Create),
        'can_edit': has_permission(user_group_id, FunctionIds.ManageInsuranceCategories, ActionIds.Edit),
        'can_delete': has_permission(user_group_id, FunctionIds.ManageInsuranceCategories, ActionIds.Delete),
        'segment': 'insurance_category',
    })


def category_create(request):
    if 'username' not in request.session:
        return redirect('employee:login')
    user_group_id = request.session.get('group_id', None)
    if not has_permission(user_group_id, FunctionIds.ManageInsuranceCategories, ActionIds.Create):
        messages.error(request, "You do not have permission to create insurance categories.")
        return redirect('categories:category_list')

    if request.method == 'POST':
        form = InsuranceCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Insurance category created successfully!')
            return redirect('categories:category_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = InsuranceCategoryForm()
    return render(request, 'categories/create.html', {'form': form, 'segment': 'insurance_category'})


def category_update(request, pk):
    if 'username' not in request.session:
        return redirect('employee:login')
    user_group_id = request.session.get('group_id', None)
    if not has_permission(user_group_id, FunctionIds.ManageInsuranceCategories, ActionIds.Edit):
        messages.error(request, "You do not have permission to edit insurance categories.")
        return redirect('categories:category_list')

    category = get_object_or_404(InsuranceCategories, pk=pk)
    if request.method == 'POST':
        form = InsuranceCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Insurance category updated successfully!')
            return redirect('categories:category_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = InsuranceCategoryForm(instance=category)
    return render(request, 'categories/update.html', {'form': form, 'category': category, 'segment': 'insurance_category'})


def category_delete(request, pk):
    if 'username' not in request.session:
        return redirect('employee:login')
    user_group_id = request.session.get('group_id', None)
    if not has_permission(user_group_id, FunctionIds.ManageInsuranceCategories, ActionIds.Delete):
        messages.error(request, "You do not have permission to delete insurance categories.")
        return redirect('categories:category_list')

    category = get_object_or_404(InsuranceCategories, pk=pk)
    if request.method == 'POST':
        with transaction.atomic():
            InsurancePriceList.objects.filter(insurance_category=category).delete()
            category.delete()
            messages.success(request, 'Insurance category deleted successfully!')
        return redirect('categories:category_list')
    return redirect('categories:category_list')


def edit_price_list(request):
    if 'username' not in request.session:
        return redirect('employee:login')
    user_group_id = request.session.get('group_id', None)
    if not has_permission(user_group_id, FunctionIds.ManageInsurancePriceList, ActionIds.Edit):
        messages.error(request, "You do not have permission to edit price list.")
        return redirect('employee:login')

    PriceListFormSet = modelformset_factory(InsurancePriceList, form=InsurancePriceListForm, extra=0)
    queryset = InsurancePriceList.objects.select_related('insurance_category', 'duration').all()

    if request.method == 'POST':
        formset = PriceListFormSet(request.POST, queryset=queryset)
        if formset.is_valid():
            formset.save()
            messages.success(request, 'Price list updated successfully!')
            return redirect('categories:category_list')
        else:
            print("Formset errors:", formset.errors)
            print("Non-form errors:", formset.non_form_errors())
            messages.error(request, 'Please correct the errors below.')
    else:
        formset = PriceListFormSet(queryset=queryset)

    categories = InsuranceCategories.objects.all()
    durations = Duration.objects.all()
    age_ranges = InsurancePriceList.objects.values('min_age', 'max_age').distinct().order_by('min_age')
    return render(request, 'categories/edit_price_list.html', {
        'formset': formset,
        'categories': categories,
        'durations': durations,
        'age_ranges': age_ranges,
        'can_add': has_permission(user_group_id, FunctionIds.ManageInsuranceCategories, ActionIds.Create),
        'can_edit': has_permission(user_group_id, FunctionIds.ManageInsuranceCategories, ActionIds.Edit),
        'can_delete': has_permission(user_group_id, FunctionIds.ManageInsuranceCategories, ActionIds.Delete),
        'segment': 'insurance_category',
    })


def update_max_coverage(request):
    if 'username' not in request.session:
        return redirect('employee:login')
    user_group_id = request.session.get('group_id', None)
    if not has_permission(user_group_id, FunctionIds.ManageInsurancePriceList, ActionIds.Edit):
        messages.error(request, "You do not have permission to update max coverage rate.")
        return redirect('home')

    categories = InsuranceCategories.objects.all()

    category_max_coverage = {}
    for category in categories:
        first_price = InsurancePriceList.objects.filter(insurance_category=category).first()
        category_max_coverage[category.id] = first_price.max_coverage_rate if first_price else 0

    if request.method == 'POST':
        with transaction.atomic():
            updated_count = 0
            for category in categories:
                max_coverage_input = request.POST.get(f'max_coverage_{category.id}')
                if max_coverage_input:
                    try:
                        new_value = Decimal(max_coverage_input)
                        if 0 <= new_value <= Decimal('99.99'):
                            updated = InsurancePriceList.objects.filter(
                                insurance_category=category
                            ).update(max_coverage_rate=new_value)
                            updated_count += updated
                        else:
                            messages.error(request, f'Invalid value for {category.name}: must be 0-99.99')
                    except (InvalidOperation, ValueError):
                        messages.error(request, f'Invalid number for {category.name}')

            if updated_count > 0:
                messages.success(request, f'Max coverage rate updated successfully for {updated_count} records!')
            else:
                messages.info(request, 'No changes were made.')

        return redirect('categories:category_list')

    return render(request, 'categories/update_max_coverage.html', {
        'categories': categories,
        'category_max_coverage': category_max_coverage,
        'can_edit': has_permission(user_group_id, FunctionIds.ManageInsurancePriceList, ActionIds.Edit),
        'segment': 'insurance_category',
    })