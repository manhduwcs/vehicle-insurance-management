from django.db import models

class Customer(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  
    fullname = models.CharField(db_column='Fullname', max_length=100, blank=True, null=True)
    address = models.TextField(db_column='Address', blank=True, null=True)
    email = models.CharField(db_column='Email', unique=True, max_length=100, blank=True, null=True)
    phone = models.CharField(db_column='Phone', unique=True, max_length=20, blank=True, null=True)
    username = models.CharField(db_column='Username', unique=True, max_length=50, blank=True, null=True)
    password = models.CharField(db_column='Password', max_length=255, blank=True, null=True)

    class Meta:
        managed = False  
        db_table = 'Customers'

    def __str__(self):
        return f"{self.fullname} ({self.username})"