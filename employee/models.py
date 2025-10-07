# employee/models.py
from django.db import models
from permissions.models import GroupsUsers  # Import from app permissions

class Employees(models.Model):
    username = models.CharField(max_length=50, unique=True)
    fullname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=255)  # Plain text temporarily
    group = models.ForeignKey(GroupsUsers, on_delete=models.SET_NULL, null=True, blank=True, related_name='employees', db_column='GroupID')

    class Meta:
        db_table = 'Employees'

    def __str__(self):
        return self.username
