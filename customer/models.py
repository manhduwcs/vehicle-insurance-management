from django.db import models
from permissions.models import GroupsUsers

class Customer(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  
    fullname = models.CharField(db_column='Fullname', max_length=100, blank=True, null=True)
    address = models.TextField(db_column='Address', blank=True, null=True)
    email = models.CharField(db_column='Email', unique=True, max_length=100, blank=True, null=True)
    phone = models.CharField(db_column='Phone', unique=True, max_length=20, blank=True, null=True)
    username = models.CharField(db_column='Username', unique=True, max_length=50, blank=True, null=True)
    password = models.CharField(db_column='Password', max_length=255, blank=True, null=True)
    identify_number = models.CharField(db_column='IdentifyNumber', max_length=50, blank=True, null=True)
    identify_address = models.CharField(db_column='IdentifyAddress', max_length=255, blank=True, null=True)
    identify_date = models.DateField(db_column='IdentifyDate', blank=True, null=True)
    issuing_authority = models.CharField(db_column='IssuingAuthority', max_length=255, blank=True, null=True)
    tax_id = models.CharField(db_column='TaxID', max_length=50, blank=True, null=True)
    group_id = models.ForeignKey(GroupsUsers,on_delete=models.SET_NULL,  db_column='GroupID',
        blank=True,
        null=True)
    class Meta:
        managed = False  
        db_table = 'Customers'
        indexes = [
            models.Index(fields=['fullname'], name='idx_customers_fullname'),
        ]

    def __str__(self):
        return f"{self.fullname} ({self.username})"
