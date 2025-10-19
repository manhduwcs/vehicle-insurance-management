from django.db import models
from categories.models import Duration, InsuranceCategories, InsurancePriceList
from vehicle.models import VehicleType, Vehicle

# class VehicleTypes(models.Model):
#     Name = models.CharField(max_length=255)
#     Fee = models.DecimalField(max_digits=10, decimal_places=2)
#     Description = models.TextField(blank=True)
#     MaxPersonalCompensation = models.DecimalField(max_digits=15, decimal_places=2)
#     MaxPropertyCompensation = models.DecimalField(max_digits=15, decimal_places=2)

#     class Meta:
#         db_table = 'VehicleTypes'

# class Vehicles(models.Model):
#     Name = models.CharField(max_length=255)
#     CustomerID = models.ForeignKey('accounts.Customer', on_delete=models.CASCADE, db_column='CustomerID')
#     Model = models.CharField(max_length=255)
#     VehicleTypeID = models.ForeignKey(VehicleTypes, on_delete=models.CASCADE, db_column='VehicleTypeID')
#     PurchasePrice = models.DecimalField(max_digits=15, decimal_places=2)
#     BodyNumber = models.CharField(max_length=50)
#     EngineNumber = models.CharField(max_length=50)
#     Number = models.CharField(max_length=50)
#     RegistrationDate = models.DateField()

#     class Meta:
#         db_table = 'Vehicles'

# class InsuranceCategories(models.Model):
#     Name = models.CharField(max_length=255)
#     Description = models.TextField(blank=True)
#     Images = models.TextField(blank=True)

#     class Meta:
#         db_table = 'InsuranceCategories'

# class Duration(models.Model):
#     Months = models.DecimalField(max_digits=5, decimal_places=2)

#     class Meta:
#         db_table = 'Duration'


class Depreciations(models.Model):
    Age = models.IntegerField()
    Rate = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        db_table = 'Depreciations'


class ContractStatus(models.TextChoices):
    AWAITING = 'Awaiting', 'Awaiting'
    PENDING = 'Pending', 'Pending'
    REJECTED = 'Rejected', 'Rejected'
    ACTIVED = 'Actived', 'Actived'
    CANCELED = 'Canceled', 'Canceled'
    INACTIVED = 'Inactived', 'Inactived'

    @classmethod
    def transitions(cls):
        return {
            cls.AWAITING: [cls.AWAITING, cls.PENDING, cls.REJECTED, cls.CANCELED],
            cls.PENDING: [cls.PENDING, cls.ACTIVED, cls.REJECTED, cls.CANCELED],
            cls.ACTIVED: [cls.ACTIVED, cls.INACTIVED],
            cls.INACTIVED: [],  
            cls.REJECTED: [],   
            cls.CANCELED: []    
        }

    @classmethod
    def can_transition(cls, current, new):
        """Check if status change is allowed."""
        return new in cls.transitions().get(current, [])


# class InsurancePriceList(models.Model):
#     InsuranceCategoryID = models.ForeignKey(InsuranceCategories, on_delete=models.CASCADE, db_column='InsuranceCategoryID')
#     DurationID = models.ForeignKey(Duration, on_delete=models.CASCADE, db_column='DurationID')
#     MinAge = models.IntegerField()
#     MaxAge = models.IntegerField()
#     Rate = models.DecimalField(max_digits=5, decimal_places=2)

#     class Meta:
#         db_table = 'InsurancePriceList'

class Contracts(models.Model):
    contract_no = models.CharField(max_length=255, unique=True, db_column='ContractNo')
    created_by = models.ForeignKey('customer.Customer', on_delete=models.CASCADE, db_column='CreatedBy', related_name='created_contracts')
    vehicle = models.ForeignKey('vehicle.Vehicle', on_delete=models.CASCADE, db_column='VehicleID')
    insurance_category = models.ForeignKey('categories.InsuranceCategories', on_delete=models.CASCADE, db_column='InsuranceCategoryID')
    estimate_value = models.DecimalField(max_digits=15, decimal_places=2, null=True, db_column='EstimateValue')
    estimate_premium = models.DecimalField(max_digits=15, decimal_places=2, db_column='EstimatePremium')
    duration = models.ForeignKey(Duration, on_delete=models.CASCADE, db_column='DurationID')
    deductible_value = models.DecimalField(max_digits=15, decimal_places=2, null=True, db_column='DeductibleValue')
    deductible_addon = models.DecimalField(max_digits=15, decimal_places=2, null=True, db_column='DeductibleAddon')
    actual_value = models.DecimalField(max_digits=15, decimal_places=2, null=True, db_column='ActualValue')
    actual_premium = models.DecimalField(max_digits=15, decimal_places=2, null=True, db_column='ActualPremium')
    fixed_deduction = models.DecimalField(max_digits=15, decimal_places=2, null=True, db_column='FixedDeduction')
    max_person_compensation = models.DecimalField(max_digits=15, decimal_places=2, null=True, db_column='MaxPersonCompensation')
    max_property_compensation = models.DecimalField(max_digits=15, decimal_places=2, null=True, db_column='MaxPropertyCompensation')
    available_person_compensation = models.DecimalField(max_digits=15, decimal_places=2, null=True, db_column='AvailablePersonCompensation')
    available_property_compensation = models.DecimalField(max_digits=15, decimal_places=2, null=True, db_column='AvailablePropertyCompensation')
    start_date = models.DateField(null=True, db_column='StartDate')
    status = models.CharField(max_length=20, choices=[
        ('Awaiting', 'Awaiting'),
        ('Pending', 'Pending'),
        ('Rejected', 'Rejected'),
        ('Actived', 'Actived'),
        ('Canceled', 'Canceled'),
        ('Inactived', 'Inactived'),
    ], db_column='Status')
    note = models.TextField(blank=True, db_column='Note')
    updated_by = models.ForeignKey('employee.Employees', on_delete=models.SET_NULL, null=True, db_column='UpdatedBy')
    created_at = models.DateTimeField(auto_now_add=True, db_column='CreatedAt')
    updated_at = models.DateTimeField(auto_now=True, db_column='UpdatedAt')

    class Meta:
        db_table = 'Contracts'
