from django.db import models

class Expenses(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField()
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    date = models.DateField()

    class Meta:
        db_table = 'Expenses'
        verbose_name = 'Expense'
        verbose_name_plural = 'Expenses'

    def __str__(self):
        return f"{self.content} - {self.amount}"


# Create your models here.
