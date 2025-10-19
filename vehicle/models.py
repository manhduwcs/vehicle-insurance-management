from django.db import models
from customer.models import Customer

class VehicleType(models.Model):
    name = models.CharField(max_length=50, db_column="Name")
    fee = models.DecimalField(max_digits=15, decimal_places=2, db_column="Fee")
    description = models.TextField(blank=True, null=True, db_column="Description")
    max_personal_compensation = models.DecimalField(max_digits=15, decimal_places=2, db_column="MaxPersonalCompensation")
    max_property_compensation = models.DecimalField(max_digits=15, decimal_places=2, db_column="MaxPropertyCompensation")

    class Meta:
        db_table = 'VehicleTypes'  
        verbose_name = "Vehicle Type"
        verbose_name_plural = "Vehicle Types"

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    name = models.CharField(max_length=100, db_column="Name")
    customer = models.ForeignKey('customer.Customer', on_delete=models.CASCADE, db_column="CustomerID")
    model = models.CharField(max_length=50, db_column="Model")
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.CASCADE, db_column="VehicleTypeID")
    purchase_price = models.DecimalField(max_digits=15, decimal_places=2, db_column="PurchasePrice")
    body_number = models.CharField(max_length=50, db_column="BodyNumber")
    engine_number = models.CharField(max_length=50, db_column="EngineNumber")
    number = models.CharField(max_length=20, db_column="Number")
    registration_date = models.DateField(db_column="RegistrationDate")

    class Meta:
        db_table = "Vehicles"

    def __str__(self):
        return self.name

class Claim(models.Model):
    """
    Represents an insurance claim filed by a customer for a specific vehicle and contract.
    """

    claim_no = models.CharField(max_length=255, unique=True, db_column="ClaimNo")

    customer = models.ForeignKey(
        "customer.Customer",
        on_delete=models.CASCADE,
        db_column="CustomerID",
        related_name="claims",
    )

    vehicle = models.ForeignKey(
        "Vehicle",
        on_delete=models.CASCADE,
        db_column="VehicleID",
        related_name="claims",
    )

    contract = models.ForeignKey(
        "contracts.Contracts",
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
