from django import forms
from .models import GroupsUsers, Functions, Actions

class GroupForm(forms.ModelForm):
    class Meta:
        model = GroupsUsers
        fields = ['group_name', 'description']
        widgets = {
            'group_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def clean_group_name(self):
        group_name = self.cleaned_data['group_name']
        exclude_id = self.instance.id if self.instance else None
        if GroupsUsers.objects.filter(group_name=group_name).exclude(id=exclude_id).exists():
            raise forms.ValidationError("Group's name already exists.")
        return group_name