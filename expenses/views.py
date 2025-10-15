from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Expenses
from .forms import ExpenseForm
from employee.views import has_permission
from permissions.constants import FunctionIds, ActionIds


def expense_list(request):
    if 'username' not in request.session:
        return redirect('employee:login')
    user_group_id = request.session.get('group_id', None)
    if not has_permission(user_group_id, FunctionIds.ManageExpenses, ActionIds.View):
        messages.error(request, "You do not have permission to view expenses.")
        return redirect('employee:employee_list')

    expenses = Expenses.objects.all()
    return render(request, 'expenses/list.html', {
        'expenses': expenses,
        'can_add': has_permission(user_group_id, FunctionIds.ManageExpenses, ActionIds.Create),
        'can_edit': has_permission(user_group_id, FunctionIds.ManageExpenses, ActionIds.Edit),
        'can_delete': has_permission(user_group_id, FunctionIds.ManageExpenses, ActionIds.Delete),
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
    return render(request, 'expenses/create.html', {'form': form})


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
    return render(request, 'expenses/update.html', {'form': form, 'expense': expense})


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


from django.shortcuts import render

# Create your views here.
