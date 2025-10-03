from django.core.management.base import BaseCommand
from discount.models import Discount
from insurance_category.models import InsuranceCategory
from customer.models import Customer

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
        sample_data_customer = [
    {"fullname": "John Smith", "address": "123 Main St, New York, NY 10001", "email": "john.smith@email.com", "phone": "(212) 555-0101", "username": "johnsmith", "password": "123456"},
    {"fullname": "Emily Johnson", "address": "456 Oak Ave, Los Angeles, CA 90210", "email": "emily.johnson@gmail.com", "phone": "(310) 555-0202", "username": "emilyjohnson", "password": "123456"},
    {"fullname": "Michael Brown", "address": "789 Pine Rd, Chicago, IL 60601", "email": "michael.brown@yahoo.com", "phone": "(312) 555-0303", "username": "michaelbrown", "password": "123456"},
    {"fullname": "Sarah Davis", "address": "101 Elm St, Houston, TX 77001", "email": "sarah.davis@outlook.com", "phone": "(713) 555-0404", "username": "sarahdavis", "password": "123456"},
    {"fullname": "David Wilson", "address": "202 Maple Dr, Phoenix, AZ 85001", "email": "david.wilson@protonmail.com", "phone": "(602) 555-0505", "username": "davidwilson", "password": "123456"},
    {"fullname": "Jessica Garcia", "address": "303 Cedar Ln, Philadelphia, PA 19101", "email": "jessica.garcia@mail.com", "phone": "(215) 555-0606", "username": "jessicagarcia", "password": "123456"},
    {"fullname": "Robert Martinez", "address": "404 Birch Blvd, San Antonio, TX 78201", "email": "robert.martinez@icloud.com", "phone": "(210) 555-0707", "username": "robertmartinez", "password": "123456"},
    {"fullname": "Ashley Rodriguez", "address": "505 Walnut Way, San Diego, CA 92101", "email": "ashley.rodriguez@gmail.com", "phone": "(619) 555-0808", "username": "ashleyrodriguez", "password": "123456"},
    {"fullname": "Christopher Lee", "address": "606 Spruce St, Dallas, TX 75201", "email": "christopher.lee@yahoo.com", "phone": "(214) 555-0909", "username": "christopherlee", "password": "123456"},
    {"fullname": "Amanda Taylor", "address": "707 Ash Ave, San Jose, CA 95101", "email": "amanda.taylor@outlook.com", "phone": "(408) 555-1010", "username": "amandataylor", "password": "123456"},
    {"fullname": "Daniel Anderson", "address": "808 Poplar Pl, Austin, TX 78701", "email": "daniel.anderson@protonmail.com", "phone": "(512) 555-1111", "username": "danielanderson", "password": "123456"},
    {"fullname": "Megan Thomas", "address": "909 Magnolia Blvd, Portland, OR 97201", "email": "megan.thomas@mail.com", "phone": "(503) 555-1212", "username": "meganthomas", "password": "123456"},
    {"fullname": "Kevin Jackson", "address": "1010 Willow Way, Columbus, OH 43201", "email": "kevin.jackson@icloud.com", "phone": "(614) 555-1313", "username": "kevinjackson", "password": "123456"}
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
        
        for data in sample_data_customer:
            obj, created = Customer.objects.get_or_create(email=data["email"], defaults=data)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created Customer: {obj.fullname}'))
            else:
                self.stdout.write(f'Already exists Customer: {obj.fullname}')