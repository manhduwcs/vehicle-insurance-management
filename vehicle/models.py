from django.db import models
from customer.models import Customer

from django.db import models

class VehicleType(models.Model):
    name = models.CharField(max_length=255)
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    max_personal_compensation = models.DecimalField(max_digits=15, decimal_places=2)
    max_property_compensation = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        db_table = 'VehicleTypes'  
        verbose_name = "Vehicle Type"
        verbose_name_plural = "Vehicle Types"

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    name = models.CharField(max_length=100, db_column="Name")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, db_column="CustomerID")
    model = models.CharField(max_length=50, db_column="Model")
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.CASCADE, db_column="TypeID")
    rate = models.DecimalField(max_digits=15, decimal_places=2, db_column="Rate")
    body_number = models.CharField(max_length=50, db_column="BodyNumber")
    engine_number = models.CharField(max_length=50, db_column="EngineNumber")
    number = models.CharField(max_length=20, db_column="Number")
    registration_date = models.DateField(db_column="RegistrationDate")

    class Meta:
        db_table = "Vehicles"

    def __str__(self):
        return self.name

class Claim(models.Model):
    claim_no = models.CharField(max_length=255, unique=True)
    customer = models.ForeignKey('admin_soft.Customer', on_delete=models.CASCADE)
    vehicle = models.ForeignKey('Vehicle', on_delete=models.CASCADE)
    contract = models.ForeignKey('contracts.Contracts', on_delete=models.CASCADE)
    place = models.TextField()
    date = models.DateField()
    human_damage = models.DecimalField(max_digits=15, decimal_places=2)
    property_damage = models.DecimalField(max_digits=15, decimal_places=2)
    deduction = models.DecimalField(max_digits=15, decimal_places=2)
    personal_compensation = models.DecimalField(max_digits=15, decimal_places=2)
    property_compensation = models.DecimalField(max_digits=15, decimal_places=2)
    note = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Completed', 'Completed'),
        ('Rejected', 'Rejected')
    ], default='Pending')
