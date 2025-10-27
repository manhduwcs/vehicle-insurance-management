# employee/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from app_helper.views import notify
from accounts.forms import hash_password
from .tokens import employee_token_generator as default_token_generator
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator


# from accounts.forms import hash_password
from .models import Employees
from .forms import EmployeeForm, LoginForm, ChangePasswordForm, EmployeeUpdateForm, EmployeePasswordResetForm, EmployeeSetPasswordForm
from django.db.models import Q
from permissions.views import has_permission
from permissions.constants import FunctionIds, ActionIds
from django.http import JsonResponse
from django.urls import reverse
from django.template.loader import render_to_string
from django.contrib.auth.hashers import check_password, make_password
from django.conf import settings
from django.core.mail import send_mail


# @login_required
def employee_list(request):
    if "username" not in request.session:
        return redirect("employee:login")
    group_id = request.session.get("group_id", None)
    if not has_permission(group_id, FunctionIds.ManageEmployeesByAdmin, ActionIds.View):
        messages.error(request, "You do not have permission to view the employees list.")
        return redirect("home")

    # get params
    search = request.GET.get('search', '')
    page = request.GET.get('page', 1)

    # query employees with select_related
    employees = Employees.objects.select_related('group')

    # search
    if search:
        employees = employees.filter(
            Q(username__icontains=search) |
            Q(fullname__icontains=search) |
            Q(email__icontains=search) |
            Q(phone__icontains=search)
        )

    # add order_by to fix UnorderedObjectListWarning
    employees = employees.order_by('-id')

    # Pagination
    paginator = Paginator(employees, 10)  # 10 items/page
    page_obj = paginator.get_page(page)

    # get permissions
    can_add = has_permission(group_id, FunctionIds.ManageEmployeesByAdmin, ActionIds.Create)
    can_edit = has_permission(group_id, FunctionIds.ManageEmployeesByAdmin, ActionIds.Edit)
    can_delete = has_permission(group_id, FunctionIds.ManageEmployeesByAdmin, ActionIds.Delete)

    # AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        table_body = render(request, 'employee/_table_body.html', {
            'employees': page_obj,
            'can_edit': can_edit,
            'can_delete': can_delete,
        }).content.decode('utf-8')
        pagination = render(request, 'employee/_pagination.html', {'page_obj': page_obj}).content.decode('utf-8')
        return JsonResponse({
            'table_body': table_body,
            'pagination': pagination,
        })

    # Render full page
    return render(
        request,
        "employee/list.html",
        {
            "segment": "employee",
            "employees": page_obj,
            "search": search,
            "can_add": can_add,
            "can_edit": can_edit,
            "can_delete": can_delete,
        },
    )


def employee_create(request):
    if "username" not in request.session:
        return redirect("employee:login")
    group_id = request.session.get("group_id", None)
    if not has_permission(group_id, FunctionIds.ManageEmployeesByAdmin, ActionIds.Create):
        messages.error(request, "You do not have permission to add new employee.")
        return redirect("employee:employee_list")
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Employee added successfully!")
            return redirect("employee:employee_list")
    else:
        form = EmployeeForm()
    return render(
        request, "employee/create.html", {"form": form, "segment": "employee"}
    )


# @login_required
def employee_update(request, pk):
    if "username" not in request.session:
        return redirect("employee:login")
    group_id = request.session.get("group_id", None)
    if not has_permission(group_id, FunctionIds.ManageEmployeesByAdmin, ActionIds.Edit):
        messages.error(request, "You do not have permission to update employee.")
        return redirect("employee:employee_list")
    employee = get_object_or_404(Employees, pk=pk)
    if request.method == "POST":
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            if (
                not form.cleaned_data["password"]
                and not form.cleaned_data["re_password"]
            ):
                form.instance.password = employee.password
            else:
                form.instance.password = form.cleaned_data["password"]
            form.save()
            messages.success(request, "Employee updated successfully!")
            return redirect("employee:employee_list")
    else:
        form = EmployeeForm(instance=employee)
    return render(
        request, "employee/update.html", {"form": form, "segment": "employee"}
    )

# @login_required
def employee_delete(request, pk):
    if "username" not in request.session:
        return redirect("employee:login")
    group_id = request.session.get("group_id", None)
    if not has_permission(group_id, FunctionIds.ManageEmployeesByAdmin, ActionIds.Delete):
        messages.error(request, "You do not have permission to delete employee.")
        return redirect("employee:employee_list")
    employee = get_object_or_404(Employees, pk=pk)
    employee.delete()
    messages.success(request, "Employee deleted successfully!")
    return redirect("employee:employee_list")


def employee_detail(request, pk):
    if "username" not in request.session:
        return redirect("employee:login")
    group_id = request.session.get("group_id", None)
    if not has_permission(group_id, FunctionIds.ManageEmployeesByAdmin, ActionIds.View):
        messages.error(request, "You do not have permission to view employee details.")
        return redirect("employee:employee_list")
    employee = get_object_or_404(Employees, pk=pk)
    return render(
        request, "employee/detail.html",
        {"employee": employee,
                "segment": "employee",
                'can_edit': has_permission(group_id, FunctionIds.ManageEmployeesByAdmin, ActionIds.Edit),
                'can_delete': has_permission(group_id, FunctionIds.ManageEmployeesByAdmin, ActionIds.Delete),}
    )


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            employee = form.cleaned_data["employee"]
            request.session["username"] = employee.username
            request.session["fullname"] = employee.fullname
            request.session["email"] = employee.email
            request.session["phone"] = employee.phone
            request.session["group_id"] = employee.group.id if employee.group else None
            return redirect("home")
        # else:
        #     notify(request, "Invalid username/email or password.", "error")
    else:
        form = LoginForm()
    return render(request, "employee/login.html", {"form": form})

def employee_profile(request):
    if "username" not in request.session:
        return redirect("employee:login")
    group_id = request.session.get("group_id", None)
    print("groupID of employee: ", group_id)
    if not has_permission(group_id, FunctionIds.ManageEmployeesByEmployees, ActionIds.View):
        messages.error(request, "You do not have permission to view profile.")
        return redirect("home")

    employee = get_object_or_404(Employees, username=request.session["username"])
    return render(request, "employee/profile.html",
                  {"employee": employee,
                   "segment": "employee",
                   'can_edit': has_permission(group_id, FunctionIds.ManageEmployeesByEmployees, ActionIds.Edit)})

def change_password(request):
    if "username" not in request.session:
        return redirect("employee:login")
    group_id = request.session.get("group_id", None)
    if not has_permission(group_id, FunctionIds.ManageEmployeesByEmployees, ActionIds.Edit):
        return redirect("employee:profile")

    employee = get_object_or_404(Employees, username=request.session["username"])
    if request.method == "POST" and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        form = ChangePasswordForm(employee, request.POST)
        if form.is_valid():
            employee.password = form.cleaned_data["new_password"]
            employee.save()
            return JsonResponse({
                'success': True,
                'message': "Password changed successfully. Please login again!"
            })
        else:
            return JsonResponse({
                'success': False,
                'form_html': render_to_string('employee/change_password_form.html', {'form': form})
            })
    else:
        form = ChangePasswordForm(employee)
    return render(request, "employee/change_password.html", {"employee": employee, "form": form, "segment": "employee"})


def reset_password_view(request):
    if request.method == "POST":
        form = EmployeePasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            employee = Employees.objects.get(email=email)

            uid = urlsafe_base64_encode(force_bytes(employee.pk))
            token = default_token_generator.make_token(employee)

            reset_url = request.build_absolute_uri(
                reverse('employee:password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
            )

            expiry_time_minutes = int(getattr(settings, 'PASSWORD_RESET_TIMEOUT', 300) / 60)

            subject = "Password Reset Request"
            message = f"""Hi {employee.fullname},

            You requested to reset your password. Click the link below to reset it:

            {reset_url}

            This link will expire in {expiry_time_minutes:.0f} minute(s).

            If you didn't request this, please ignore this email.

            Best regards,
            Your Team"""
            from_email = "no-reply@yourapp.com"

            send_mail(subject, message, from_email, [email])

            messages.success(request, "A password reset link has been sent to your email.")
            return redirect('employee:password_change_done')
    else:
        form = EmployeePasswordResetForm()

    return render(request, 'employee/password_reset.html', {'form': form})


def password_reset_done_view(request):
    return render(request, 'employee/password_reset_done.html')


def password_reset_confirm_view(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        employee = Employees.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Employees.DoesNotExist):
        customer = None

    if employee is not None and default_token_generator.check_token(employee, token):
        if request.method == "POST":
            form = EmployeeSetPasswordForm(employee, request.POST)
            if form.is_valid():
                new_password = form.cleaned_data["new_password1"]
                employee.password = hash_password(new_password)
                employee.save()
                messages.success(request, "Your password has been reset successfully.")
                return redirect("employee:login")
        else:
            form = EmployeeSetPasswordForm(employee)
        return render(request, "employee/password_reset_confirm.html", {"form": form, "validlink": True})
    else:
        messages.error(request, "The password reset link is invalid or has expired.")
        return render(request, "employee/password_reset_confirm.html", {"validlink": False})
