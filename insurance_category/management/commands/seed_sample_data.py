from django.core.management.base import BaseCommand
from discount.models import Discount
from insurance_category.models import InsuranceCategory

class Command(BaseCommand):
    help = "Seed sample insurance categories"

    def handle(self, *args, **kwargs):

        sample_data_discount = [
            {"name": "Summer Sale", "rate": 10, "description": "10% off for summer promotion."},
            {"name": "Winter Discount", "rate": 15, "description": "15% off during winter."},
            {"name": "VIP Customer", "rate": 20, "description": "20% off for VIP members."},
            {"name": "New Year Offer", "rate": 5, "description": "5% off for New Year."},
            {"name": "Black Friday", "rate": 25, "description": "25% discount for Black Friday."},
            {"name": "Cyber Monday", "rate": 30, "description": "30% off online orders."},
            {"name": "Holiday Special", "rate": 12, "description": "12% off during holidays."},
            {"name": "Bulk Purchase", "rate": 18, "description": "18% off for bulk purchases."},
            {"name": "Loyalty Program", "rate": 8, "description": "8% off for loyal customers."},
            {"name": "Clearance Sale", "rate": 50, "description": "50% off clearance items."},
        ]

        sample_data_insurance_category = [
            {
                "name": "Compulsory Civil Liability",
                "fee": 50.00,
                "rate": 0.0,
                "type": "Mandatory",
                "description": "Covers damages to third parties required by law."
            },
            {
                "name": "Comprehensive Vehicle Insurance",
                "fee": 200.00,
                "rate": 5.0,
                "type": "Optional",
                "description": "Covers damages to your vehicle from accidents or natural events."
            },
            {
                "name": "Theft Protection",
                "fee": 80.00,
                "rate": 3.0,
                "type": "Optional",
                "description": "Covers theft or attempted theft of your vehicle."
            },
            {
                "name": "Fire and Natural Disaster",
                "fee": 70.00,
                "rate": 2.5,
                "type": "Optional",
                "description": "Covers damages caused by fire, storms, floods, or other natural disasters."
            },
            {
                "name": "Driver Personal Accident",
                "fee": 40.00,
                "rate": 1.0,
                "type": "Optional",
                "description": "Covers injuries to the driver in case of an accident."
            },
            {
                "name": "Passenger Liability",
                "fee": 35.00,
                "rate": 0.5,
                "type": "Optional",
                "description": "Covers injuries to passengers inside the vehicle."
            },
            {
                "name": "Third-Party Property Damage",
                "fee": 60.00,
                "rate": 1.5,
                "type": "Optional",
                "description": "Covers damage to other people's property caused by your vehicle."
            },
            {
                "name": "Roadside Assistance",
                "fee": 25.00,
                "rate": 0.2,
                "type": "Optional",
                "description": "Provides towing, battery jump, or emergency help on the road."
            },
            {
                "name": "Glass Coverage",
                "fee": 30.00,
                "rate": 0.3,
                "type": "Optional",
                "description": "Covers windshield and window glass damages."
            },
            {
                "name": "Legal Protection",
                "fee": 45.00,
                "rate": 0.5,
                "type": "Optional",
                "description": "Covers legal fees arising from vehicle-related disputes."
            },
        ]

        for data in sample_data_insurance_category:
            obj, created = InsuranceCategory.objects.get_or_create(name=data["name"], defaults=data)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created: {obj.name}'))
            else:
                self.stdout.write(f'Already exists: {obj.name}')

        for data in sample_data_discount:
            obj, created = Discount.objects.get_or_create(name=data["name"], defaults=data)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created: {obj.name}'))
            else:
                self.stdout.write(f'Already exists: {obj.name}')