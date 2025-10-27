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
        indexes = [
            models.Index(fields=['content'], name='idx_expenses_content'),  # Index for content
            models.Index(fields=['date'], name='idx_expenses_date'),  # Index for date
        ]

    def __str__(self):
        return f"{self.content} - {self.amount}"


# Create your models here.
