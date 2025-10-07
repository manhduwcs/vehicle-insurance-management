from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=255, db_column="Name")

    class Meta:
        db_table = "Customers"

    def __str__(self):
        return self.name
