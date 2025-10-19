from django.db import models
from vehicle.models import Vehicle
from categories.models import Duration,InsuranceCategories,InsurancePriceList


class Depreciations(models.Model):
    Age = models.IntegerField()
    Rate = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        db_table = 'Depreciations'


class Contracts(models.Model):
    ContractNo = models.CharField(max_length=255, unique=True)
    CreatedBy = models.ForeignKey('customer.Customer', on_delete=models.CASCADE, db_column='CreatedBy', related_name='created_contracts')
    VehicleID = models.ForeignKey(Vehicle, on_delete=models.CASCADE, db_column='VehicleID')
    InsuranceCategoryID = models.ForeignKey(InsuranceCategories, on_delete=models.CASCADE, db_column='InsuranceCategoryID')
    EstimateValue = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    EstimatePremium = models.DecimalField(max_digits=15, decimal_places=2)
    DurationID = models.ForeignKey(Duration, on_delete=models.CASCADE, db_column='DurationID')
    DeductibleValue = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    DeductibleAddon = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    ActualValue = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    ActualPremium = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    FixedDeduction = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    MaxPersonCompensation = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    MaxPropertyCompensation = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    AvailablePersonCompensation = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    AvailablePropertyCompensation = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    StartDate = models.DateField(null=True)
    Status = models.CharField(max_length=20, choices=[
        ('Awaiting', 'Awaiting'),
        ('Pending', 'Pending'),
        ('Rejected', 'Rejected'),
        ('Actived', 'Actived'),
        ('Canceled', 'Canceled'),
        ('Inactived', 'Inactived'),
    ])
    Note = models.TextField(blank=True)
    UpdatedBy = models.ForeignKey('employee.Employees', on_delete=models.SET_NULL, null=True, db_column='UpdatedBy')
    CreatedAt = models.DateTimeField(auto_now_add=True)
    UpdatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Contracts'
