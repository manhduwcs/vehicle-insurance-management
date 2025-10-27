from django.db import models
from vehicle_types.models import VehicleTypes

class Vehicles(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, db_column="Name")
    customer_id = models.ForeignKey('customer.Customer', on_delete=models.CASCADE, db_column="CustomerID")
    model = models.CharField(max_length=255, db_column="Model")
    vehicle_type = models.ForeignKey(VehicleTypes, on_delete=models.CASCADE, db_column="VehicleTypeID")
    purchase_price = models.DecimalField(max_digits=15, decimal_places=2, db_column="PurchasePrice")
    body_number = models.CharField(max_length=50, db_column="BodyNumber")
    engine_number = models.CharField(max_length=50, db_column="EngineNumber")
    number = models.CharField(max_length=50, db_column="Number")
    registration_date = models.DateField(db_column="RegistrationDate")

    class Meta:
        db_table = 'Vehicles'
        verbose_name = 'Vehicle'
        verbose_name_plural = 'Vehicles'
        indexes = [
            models.Index(fields=['number'], name='idx_vehicles_number'),
        ]

    def __str__(self):
        return f"{self.name} - {self.model}"