from django.db import models
# from vehicle.models import Vehicle
from customer.models import Customer
from contracts.models import Contracts
from vehicles.models import Vehicles


class Claim(models.Model):
    """
    Represents an insurance claim filed by a customer for a specific vehicle and contract.
    """

    claim_no = models.CharField(max_length=255, unique=True, db_column="ClaimNo")

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        db_column="CustomerID",
        related_name="claims",
    )

    vehicles = models.ForeignKey(
        Vehicles,
        on_delete=models.CASCADE,
        db_column="VehicleID",
        related_name="claims",
    )

    contract = models.ForeignKey(
        Contracts,
        on_delete=models.CASCADE,
        db_column="ContractID",
        related_name="claims",
    )

    place = models.TextField(db_column="Place")
    date = models.DateField(db_column="Date")

    human_damage = models.DecimalField(
        max_digits=15, decimal_places=2, db_column="HumanDamage"
    )
    property_damage = models.DecimalField(
        max_digits=15, decimal_places=2, db_column="PropertyDamage"
    )
    deduction = models.DecimalField(
        max_digits=15, decimal_places=2, db_column="Deduction"
    )

    personal_compensation = models.DecimalField(
        max_digits=15, decimal_places=2, db_column="PersonalCompensation"
    )
    property_compensation = models.DecimalField(
        max_digits=15, decimal_places=2, db_column="PropertyCompensation"
    )

    note = models.TextField(blank=True, null=True, db_column="Note")

    status = models.CharField(
        max_length=20,
        choices=[
            ("Pending", "Pending"),
            ("Approved", "Approved"),
            ("Completed", "Completed"),
            ("Rejected", "Rejected"),
        ],
        default="Pending",
        db_column="Status",
    )

    class Meta:
        db_table = "Claims"
        verbose_name = "Claim"
        verbose_name_plural = "Claims"
        ordering = ["-date"]

    def __str__(self):
        return f"Claim #{self.claim_no} - {self.status}"
