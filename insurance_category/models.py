# insurance_category/models.py
from django.db import models

class InsuranceCategory(models.Model):
    name = models.CharField(max_length=255, db_column="Name")
    fee = models.DecimalField(max_digits=10, decimal_places=2, db_column="Fee")
    rate = models.DecimalField(max_digits=5, decimal_places=2, db_column="Rate")
    type = models.CharField(max_length=255, db_column="Type")
    description = models.TextField(blank=True, null=True, db_column="Description")

    class Meta:
        db_table = "InsuranceCategories"  