from django.db import models

class Discount(models.Model):
    id = models.AutoField(primary_key=True, db_column="ID")
    name = models.CharField(max_length=255, db_column="Name")
    rate = models.DecimalField(max_digits=10, decimal_places=2, db_column="Rate")
    description = models.TextField(db_column="Description", blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "Discounts"   
