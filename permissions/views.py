from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from .models import GroupsUsers, Functions, Actions, GroupsFunctionsActions
from .forms import GroupForm
from .constants import FunctionIds, ActionIds
from employee.models import Employees
from django.contrib.auth.models import Group


def has_permission(group_id, function_name, action_name):
    cache_key = f"perm_{group_id}_{function_name}_{action_name}"
    perm = cache.get(cache_key)
    if perm is None:
        perm = GroupsFunctionsActions.objects.filter(
            group_id=group_id,
            function__function_name=function_name,
            action__action_name=action_name
        ).exists()
        cache.set(cache_key, perm, timeout=3600)  # Cache 1 hour
    return perm


def groups_list(request):
    if 'username' not in request.session:
        return redirect('employee:login')
    group_id = request.session.get('group_id', None)
    if not has_permission(group_id, FunctionIds.ManageGroupsUsers, ActionIds.View):
        messages.error(request, "You do not have permission to view the group list.")
        return redirect('/permissions/')
    groups = GroupsUsers.objects.all()
    return render(request, 'permissions/groups.html', {
        'groups': groups,
        'can_add': has_permission(group_id, FunctionIds.ManageGroupsUsers, ActionIds.Create),
        'can_edit': has_permission(group_id, FunctionIds.ManageGroupsUsers, ActionIds.Edit),
        'can_delete': has_permission(group_id, FunctionIds.ManageGroupsUsers, ActionIds.Delete),
    })

def add_group(request):
    if 'username' not in request.session:
        return redirect('employee:login')
    group_id = request.session.get('group_id', None)
    if not has_permission(group_id, FunctionIds.ManageGroupsUsers, ActionIds.Create):
        messages.error(request, "You do not have permission to add new group.")
        return redirect('permissions:groups_list')
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Group added successfully!")
            return redirect('permissions:groups_list')
    else:
        form = GroupForm()
    return render(request, 'permissions/add_group.html', {'form': form})

def edit_group(request, group_id):
    if 'username' not in request.session:
        return redirect('employee:login')
    user_group_id = request.session.get('group_id', None)
    if not has_permission(user_group_id, FunctionIds.ManageGroupsUsers, ActionIds.Edit):
        messages.error(request, "You do not have permission to update group.")
        return redirect('permissions:groups_list')
    group_obj = get_object_or_404(GroupsUsers, id=group_id)
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Group updated successfully!")
            return redirect('permissions:groups_list')
    else:
        form = GroupForm(instance=group_obj)
    return render(request, 'permissions/edit_group.html', {'form': form, 'group': group_obj})

def delete_group(request, group_id):
    if 'username' not in request.session:
        return redirect('employee:login')
    user_group_id = request.session.get('group_id', None)
    if not has_permission(user_group_id, FunctionIds.ManageGroupsUsers, ActionIds.Delete):
        messages.error(request, "You do not have permission to delete group.")
        return redirect('permissions:groups_list')
    group_obj = get_object_or_404(GroupsUsers, id=group_id)
    if request.method == 'POST':
        if Employees.objects.filter(group=group_obj).exists():
            messages.error(request, "Cannot delete group because it has associated users.")
        else:
            group_obj.delete()
            cache.clear()
            messages.success(request, "Group deleted successfully!")
        return redirect('permissions:groups_list')
    return render(request, 'permissions/groups.html', {'groups': GroupsUsers.objects.all()})

def assign_permission(request, group_id):
    if 'username' not in request.session:
        return redirect('employee:login')
    user_group_id = request.session.get('group_id', None)
    if not has_permission(user_group_id, FunctionIds.ManageGroupsUsers, ActionIds.Edit):
        messages.error(request, "You do not have permission to delegate.")
        return redirect('permissions:groups_list')
    group_obj = get_object_or_404(GroupsUsers, id=group_id)
    functions = Functions.objects.all()
    selected_function = None
    actions = []
    selected_actions = []
    if request.method == 'POST':
        function_id = request.POST.get('function_id')
        selected_actions_post = request.POST.getlist('actions')
        if function_id:
            function = get_object_or_404(Functions, id=function_id)
            GroupsFunctionsActions.objects.filter(group=group_obj, function=function).delete()
            for action_id in selected_actions_post:
                action = get_object_or_404(Actions, id=action_id)
                GroupsFunctionsActions.objects.create(group=group_obj, function=function, action=action)
            cache.clear()
            messages.success(request, "Permission saved successfully!")
        return redirect('permissions:assign_permission', group_id=group_id)
    function_id = request.GET.get('function_id')
    if function_id:
        selected_function = get_object_or_404(Functions, id=function_id)
        actions = Actions.objects.all()
        current_perms = GroupsFunctionsActions.objects.filter(group=group_obj, function=selected_function)
        selected_actions = [perm.action.id for perm in current_perms]
    return render(request, 'permissions/permission.html', {
        'functions': functions,
        'selected_function': selected_function,
        'actions': actions,
        'selected_actions': selected_actions,
        'group': group_obj
    })

from django.shortcuts import render

# Create your views here.
