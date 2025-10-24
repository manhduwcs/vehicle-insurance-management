from django import template
from permissions.views import has_permission
from permissions.constants import FunctionIds, ActionIds

register = template.Library()

@register.filter
def can_view(user, function_action):
    group_id = user.get('group_id', None) if isinstance(user, dict) else user.session.get("group_id", None)
    if not group_id:
        return False
    function_id, action_id = function_action.split('_')
    return has_permission(group_id, FunctionIds[function_id], ActionIds[action_id])