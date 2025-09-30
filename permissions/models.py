from django.db import models

class GroupsUsers(models.Model):
    group_name = models.CharField(max_length=100, unique=True, db_column='GroupName')  # Map với 'GroupName'
    description = models.TextField(blank=True, null=True, db_column='Description')  # Map với 'Description'

    class Meta:
        db_table = 'GroupsUsers'

    def __str__(self):
        return self.group_name

class Functions(models.Model):
    function_name = models.CharField(max_length=100, unique=True, db_column='FunctionName')  # Map với 'FunctionName'
    description = models.TextField(blank=True, null=True, db_column='Description')

    class Meta:
        db_table = 'Functions'

    def __str__(self):
        return self.function_name

class Actions(models.Model):
    action_name = models.CharField(max_length=100, unique=True, db_column='ActionName')  # Map với 'ActionName'
    description = models.TextField(blank=True, null=True, db_column='Description')

    class Meta:
        db_table = 'Actions'

    def __str__(self):
        return self.action_name

class GroupsFunctionsActions(models.Model):
    group = models.ForeignKey(GroupsUsers, on_delete=models.CASCADE, db_column='GroupID')  # Map với 'GroupID'
    function = models.ForeignKey(Functions, on_delete=models.CASCADE, db_column='FunctionID')  # Map với 'FunctionID'
    action = models.ForeignKey(Actions, on_delete=models.CASCADE, db_column='ActionID')  # Map với 'ActionID'

    class Meta:
        db_table = 'GroupsFunctionsActions'
        unique_together = ('group', 'function', 'action')

    def __str__(self):
        return f"{self.group.group_name} - {self.function.function_name} - {self.action.action_name}"