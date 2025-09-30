# employee/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Employees
from .forms import EmployeeForm, LoginForm
from django.db.models import Q
from permissions.views import has_permission
from permissions.constants import FunctionIds, ActionIds

# @login_required
def employee_list(request):
    if 'username' not in request.session:
        return redirect('employee:login')
    group_id = request.session.get('group_id', None)
    if not has_permission(group_id, FunctionIds.ManageEmployees, ActionIds.View):
        messages.error(request, "You do not have permission to view the employee list.")
        return redirect('employee:employee_list')
    employees = Employees.objects.all()
    return render(request, 'employee/list.html', {
        'employees': employees,
        'can_add': has_permission(group_id, FunctionIds.ManageEmployees, ActionIds.Create),
        'can_edit': has_permission(group_id, FunctionIds.ManageEmployees, ActionIds.Edit),
        'can_delete': has_permission(group_id, FunctionIds.ManageEmployees, ActionIds.Delete),
    })



def employee_create(request):
    if 'username' not in request.session:
        return redirect('employee:login')
    group_id = request.session.get('group_id', None)
    if not has_permission(group_id, FunctionIds.ManageEmployees, ActionIds.Create):
        messages.error(request, "You do not have permission to add new employee.")
        return redirect('employee:employee_list')
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee added successfully!')
            return redirect('employee:employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'employee/create.html', {'form': form})


# @login_required
def employee_update(request, pk):
    if 'username' not in request.session:
        return redirect('employee:login')
    group_id = request.session.get('group_id', None)
    if not has_permission(group_id, FunctionIds.ManageEmployees, ActionIds.Edit):
        messages.error(request, "You do not have permission to update employee.")
        return redirect('employee:employee_list')
    employee = get_object_or_404(Employees, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            if not form.cleaned_data['password'] and not form.cleaned_data['re_password']:
                form.instance.password = employee.password
            form.save()
            messages.success(request, 'Employee updated successfully!')
            return redirect('employee:employee_list')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'employee/update.html', {'form': form})


# @login_required
def employee_delete(request, pk):
    if 'username' not in request.session:
        return redirect('employee:login')
    group_id = request.session.get('group_id', None)
    if not has_permission(group_id, FunctionIds.ManageEmployees, ActionIds.Delete):
        messages.error(request, "You do not have permission to delete employee.")
        return redirect('employee:employee_list')
    employee = get_object_or_404(Employees, pk=pk)
    employee.delete()
    messages.success(request, 'Employee deleted successfully!')
    return redirect('employee:employee_list')


def employee_detail(request, pk):
    if 'username' not in request.session:
        return redirect('employee:login')
    group_id = request.session.get('group_id', None)
    if not has_permission(group_id, FunctionIds.ManageEmployees, ActionIds.View):
        messages.error(request, "You do not have permission to view employee details.")
        return redirect('employee:employee_list')
    employee = get_object_or_404(Employees, pk=pk)
    return render(request, 'employee/detail.html', {'employee': employee})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            login_input = form.cleaned_data['login']
            password = form.cleaned_data['password']
            employee = Employees.objects.filter(
                (Q(username=login_input) | Q(email=login_input)) & Q(password=password)
            ).first()
            if employee:
                request.session['username'] = employee.username
                request.session['fullname'] = employee.fullname
                request.session['email'] = employee.email
                request.session['phone'] = employee.phone
                request.session['group_id'] = employee.group.id if employee.group else None
                # messages.success(request, 'Login successful!')
                return redirect('employee:employee_list')  # Redirect to employee list or home
            else:
                messages.error(request, 'Invalid username/email or password.')
    else:
        form = LoginForm()
    return render(request, 'employee/login.html', {'form': form})


from django.shortcuts import render

# Create your views here.
