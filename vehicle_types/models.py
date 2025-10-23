from django.db import models

class VehicleTypes(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, db_column="Name")
    fee = models.DecimalField(max_digits=10, decimal_places=2, db_column="Fee")
    description = models.TextField(blank=True, null=True, db_column="Description")
    max_personal_compensation = models.DecimalField(max_digits=15, decimal_places=2, db_column="MaxPersonalCompensation")
    max_property_compensation = models.DecimalField(max_digits=15, decimal_places=2, db_column="MaxPropertyCompensation")

    class Meta:
        db_table = 'VehicleTypes'
        verbose_name = 'Vehicle Type'
        verbose_name_plural = 'Vehicle Types'

    def __str__(self):
        return f"{self.name} - {self.fee}"