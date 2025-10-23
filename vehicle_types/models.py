from django.db import models

class VehicleTypes(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    max_personal_compensation = models.DecimalField(max_digits=15, decimal_places=2)
    max_property_compensation = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        db_table = 'VehicleTypes'
        verbose_name = 'Vehicle Type'
        verbose_name_plural = 'Vehicle Types'

    def __str__(self):
        return f"{self.name} - {self.fee}"