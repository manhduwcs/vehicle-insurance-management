from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class InsuranceCategories(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'InsuranceCategories'
        verbose_name = 'Insurance Category'
        verbose_name_plural = 'Insurance Categories'

    def __str__(self):
        return self.name

class Duration(models.Model):
    id = models.AutoField(primary_key=True)
    months = models.IntegerField()

    class Meta:
        db_table = 'Duration'
        verbose_name = 'Duration'
        verbose_name_plural = 'Durations'

    def __str__(self):
        return f"{self.months} months"

class InsurancePriceList(models.Model):
    id = models.AutoField(primary_key=True)
    insurance_category = models.ForeignKey(InsuranceCategories, on_delete=models.CASCADE, db_column='InsuranceCategoryID')
    duration = models.ForeignKey(Duration, on_delete=models.CASCADE, db_column='DurationID')
    min_age = models.IntegerField(db_column='MinAge')
    max_age = models.IntegerField(db_column='MaxAge')
    rate = models.DecimalField(max_digits=5, decimal_places=2, default=0, db_column='RatePremium')
    max_coverage_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0, db_column='MaxCoverageRate')

    class Meta:
        db_table = 'InsurancePriceList'
        verbose_name = 'Insurance Price List'
        verbose_name_plural = 'Insurance Price Lists'

    def __str__(self):
        return f"{self.insurance_category.name} - {self.duration.months} months - Age {self.min_age}-{self.max_age}"

# Automatically create 12 PriceList rows when creating a category
@receiver(post_save, sender=InsuranceCategories)
def create_price_list(sender, instance, created, **kwargs):
    if created:
        durations = Duration.objects.all()  # [12, 24, 36]
        age_groups = [(0, 3), (4, 7), (8, 10), (11, 20)]
        for duration in durations:
            for min_age, max_age in age_groups:
                InsurancePriceList.objects.create(
                    insurance_category=instance,
                    duration=duration,
                    min_age=min_age,
                    max_age=max_age,
                    rate=0,
                    max_coverage_rate=0
                )