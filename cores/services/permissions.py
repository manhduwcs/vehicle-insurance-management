from permissions.models import GroupsFunctionsActions, Actions, GroupsUsers

def get_accessible_functions(request):
    group_id = request.session.get('group_id')
    if not group_id:
        return []

    try:
        view_action = Actions.objects.get(action_name='View')
    except Actions.DoesNotExist:
        return []

    return (
        GroupsFunctionsActions.objects.filter(
            group_id=group_id,
            action=view_action
        )
        .select_related('function')
        .values_list('function__function_name', flat=True)
        .distinct()
    )
