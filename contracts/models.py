from django.db import models

class VehicleTypes(models.Model):
    Name = models.CharField(max_length=255)
    Fee = models.DecimalField(max_digits=10, decimal_places=2)
    Description = models.TextField(blank=True)
    MaxPersonalCompensation = models.DecimalField(max_digits=15, decimal_places=2)
    MaxPropertyCompensation = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        db_table = 'VehicleTypes'

class Vehicles(models.Model):
    Name = models.CharField(max_length=255)
    CustomerID = models.ForeignKey('accounts.Customer', on_delete=models.CASCADE, db_column='CustomerID')
    Model = models.CharField(max_length=255)
    VehicleTypeID = models.ForeignKey(VehicleTypes, on_delete=models.CASCADE, db_column='VehicleTypeID')
    PurchasePrice = models.DecimalField(max_digits=15, decimal_places=2)
    BodyNumber = models.CharField(max_length=50)
    EngineNumber = models.CharField(max_length=50)
    Number = models.CharField(max_length=50)
    RegistrationDate = models.DateField()

    class Meta:
        db_table = 'Vehicles'

class InsuranceCategories(models.Model):
    Name = models.CharField(max_length=255)
    Description = models.TextField(blank=True)
    Images = models.TextField(blank=True)

    class Meta:
        db_table = 'InsuranceCategories'

class Duration(models.Model):
    Months = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        db_table = 'Duration'

class Depreciations(models.Model):
    Age = models.IntegerField()
    Rate = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        db_table = 'Depreciations'

class InsurancePriceList(models.Model):
    InsuranceCategoryID = models.ForeignKey(InsuranceCategories, on_delete=models.CASCADE, db_column='InsuranceCategoryID')
    DurationID = models.ForeignKey(Duration, on_delete=models.CASCADE, db_column='DurationID')
    MinAge = models.IntegerField()
    MaxAge = models.IntegerField()
    Rate = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        db_table = 'InsurancePriceList'

class Contracts(models.Model):
    ContractNo = models.CharField(max_length=255, unique=True)
    CreatedBy = models.ForeignKey('accounts.Customer', on_delete=models.CASCADE, db_column='CreatedBy', related_name='created_contracts')
    VehicleID = models.ForeignKey(Vehicles, on_delete=models.CASCADE, db_column='VehicleID')
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
    UpdatedBy = models.ForeignKey('permissions.Employees', on_delete=models.SET_NULL, null=True, db_column='UpdatedBy')
    CreatedAt = models.DateTimeField(auto_now_add=True)
    UpdatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Contracts'
