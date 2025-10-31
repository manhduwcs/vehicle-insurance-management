from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Expenses
from .forms import ExpenseForm
from employee.views import has_permission
from permissions.constants import FunctionIds, ActionIds
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from datetime import datetime

def expense_list(request):
    if "username" not in request.session:
        return redirect("employee:login")
    group_id = request.session.get("group_id", None)
    if not has_permission(group_id, FunctionIds.ManageExpenses, ActionIds.View):
        messages.error(request, "You do not have permission to view the expenses list.")
        return redirect("home")

    # get params
    search = request.GET.get('search', '')
    from_date_str = request.GET.get('from_date', '')
    to_date_str = request.GET.get('to_date', '')
    page = request.GET.get('page', 1)

    # query expenses
    expenses = Expenses.objects.all()

    # search by content
    if search:
        expenses = expenses.filter(Q(content__icontains=search))

    # filter by date
    if from_date_str:
        try:
            from_date = datetime.strptime(from_date_str, '%Y-%m-%d').date()
            expenses = expenses.filter(date__gte=from_date)
        except ValueError:
            pass  # ignore if invalid
    if to_date_str:
        try:
            to_date = datetime.strptime(to_date_str, '%Y-%m-%d').date()
            expenses = expenses.filter(date__lte=to_date)
        except ValueError:
            pass  # ignore if invalid

    # add order_by to fix UnorderedObjectListWarning
    expenses = expenses.order_by('-date')  # order by newest

    # Pagination
    paginator = Paginator(expenses, 10)  # 10 items/page
    page_obj = paginator.get_page(page)

    # get permissions
    can_add = has_permission(group_id, FunctionIds.ManageExpenses, ActionIds.Create)
    can_edit = has_permission(group_id, FunctionIds.ManageExpenses, ActionIds.Edit)
    can_delete = has_permission(group_id, FunctionIds.ManageExpenses, ActionIds.Delete)

    # AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        table_body = render(request, 'expenses/_table_body.html', {
            'expenses': page_obj,
            'can_edit': can_edit,
            'can_delete': can_delete,
        }).content.decode('utf-8')
        pagination = render(request, 'expenses/_pagination.html', {'page_obj': page_obj}).content.decode('utf-8')
        return JsonResponse({
            'table_body': table_body,
            'pagination': pagination,
        })

    # Render full page
    return render(request, 'expenses/list.html', {
        'expenses': page_obj,
        'search': search,
        'from_date': from_date_str,
        'to_date': to_date_str,
        'can_add': can_add,
        'can_edit': can_edit,
        'can_delete': can_delete,
        'segment': 'expenses',
    })


def expense_create(request):
    if 'username' not in request.session:
        return redirect('employee:login')
    user_group_id = request.session.get('group_id', None)
    if not has_permission(user_group_id, FunctionIds.ManageExpenses, ActionIds.Create):
        messages.error(request, "You do not have permission to create expenses.")
        return redirect('expenses:expense_list')

    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Expense created successfully!')
            return redirect('expenses:expense_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ExpenseForm()
    return render(request, 'expenses/create.html', {'form': form, 'segment': 'expenses'})


def expense_update(request, pk):
    if 'username' not in request.session:
        return redirect('employee:login')
    user_group_id = request.session.get('group_id', None)
    if not has_permission(user_group_id, FunctionIds.ManageExpenses, ActionIds.Edit):
        messages.error(request, "You do not have permission to edit expenses.")
        return redirect('expenses:expense_list')

    expense = get_object_or_404(Expenses, pk=pk)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, 'Expense updated successfully!')
            return redirect('expenses:expense_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'expenses/update.html', {'form': form, 'expense': expense, 'segment': 'expenses'})


def expense_detail(request, pk):
    if 'username' not in request.session:
        return redirect('employee:login')
    user_group_id = request.session.get('group_id', None)
    if not has_permission(user_group_id, FunctionIds.ManageExpenses, ActionIds.View):
        messages.error(request, "You do not have permission to view expense details.")
        return redirect('expenses:expense_list')

    expense = get_object_or_404(Expenses, pk=pk)
    return render(request, 'expenses/detail.html', {
        'expense': expense,
        'can_edit': has_permission(user_group_id, FunctionIds.ManageExpenses, ActionIds.Edit),
        'can_delete': has_permission(user_group_id, FunctionIds.ManageExpenses, ActionIds.Delete),
        'segment': 'expenses',
    })


def expense_delete(request, pk):
    if 'username' not in request.session:
        return redirect('employee:login')
    user_group_id = request.session.get('group_id', None)
    if not has_permission(user_group_id, FunctionIds.ManageExpenses, ActionIds.Delete):
        messages.error(request, "You do not have permission to delete expenses.")
        return redirect('expenses:expense_list')

    expense = get_object_or_404(Expenses, pk=pk)
    if request.method == 'POST':
        expense.delete()
        messages.success(request, 'Expense deleted successfully!')
        return redirect('expenses:expense_list')
    return redirect('expenses:expense_list')



# Create your views here.
