from django.db import models

class InsuranceCategory(models.Model):
    id = models.AutoField(primary_key=True, db_column="ID")
    name = models.CharField(max_length=255, db_column="Name")
    description = models.TextField(blank=True, null=True, db_column="Description")

    # class Meta:
    #     db_table = "InsuranceCategories"
