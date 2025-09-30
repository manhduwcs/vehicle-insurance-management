from django.contrib import admin
from .models import GroupsUsers, Functions, Actions, GroupsFunctionsActions

@admin.register(GroupsUsers)
class GroupsUsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'group_name', 'description')
    search_fields = ('group_name',)

@admin.register(Functions)
class FunctionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'function_name', 'description')
    search_fields = ('function_name',)

@admin.register(Actions)
class ActionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'action_name', 'description')
    search_fields = ('action_name',)

@admin.register(GroupsFunctionsActions)
class GroupsFunctionsActionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'group', 'function', 'action')
    list_filter = ('group', 'function', 'action')