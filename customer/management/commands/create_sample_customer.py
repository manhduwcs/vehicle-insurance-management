from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth.hashers import make_password
from django.utils import timezone

from customer.models import Customer  


class Command(BaseCommand):
    help = "Create sample customers (password='123456' for all)."

    def handle(self, *args, **options):
        customers_data = [
            {
                "username": "johnsmith",
                "password_plain": "123456",
                "fullname": "John Smith",
                "address": "12 Nguyen Trai, District 1, Ho Chi Minh City",
                "email": "john.smith@example.com",
                "phone": "0903123456",
                # extra ignored fields:
                "identify_number": "123456789",
                "identify_address": "Ho Chi Minh City",
                "identify_date": "2020-05-12",
                "issuing_authority": "Police Dept HCM",
                "tax_id": "TX00123",
            },
            {
                "username": "emilytran",
                "password_plain": "123456",
                "fullname": "Emily Tran",
                "address": "45 Cau Giay, Hanoi",
                "email": "emily.tran@example.com",
                "phone": "0987234567",
                "identify_number": "987654321",
                "identify_address": "Hanoi",
                "identify_date": "2021-03-20",
                "issuing_authority": "Police Dept Hanoi",
                "tax_id": "TX00456",
            },
            {
                "username": "michaelle",
                "password_plain": "123456",
                "fullname": "Michael Le",
                "address": "89 Le Loi, Da Nang",
                "email": "michael.le@example.com",
                "phone": "0934567890",
                "identify_number": "223344556",
                "identify_address": "Da Nang",
                "identify_date": "2021-08-09",
                "issuing_authority": "Police Dept Da Nang",
                "tax_id": "TX00789",
            },
            {
                "username": "hannahpham",
                "password_plain": "123456",
                "fullname": "Hannah Pham",
                "address": "21 Nguyen Hue, Hue City",
                "email": "hannah.pham@example.com",
                "phone": "0976543210",
                "identify_number": "112233445",
                "identify_address": "Hue",
                "identify_date": "2022-01-12",
                "issuing_authority": "Police Dept Hue",
                "tax_id": "TX01001",
            },
            {
                "username": "ethannam",
                "password_plain": "123456",
                "fullname": "Ethan Nam",
                "address": "5 Ly Thuong Kiet, Hai Phong",
                "email": "ethan.nam@example.com",
                "phone": "0912789345",
                "identify_number": "334455667",
                "identify_address": "Hai Phong",
                "identify_date": "2020-09-30",
                "issuing_authority": "Police Dept Hai Phong",
                "tax_id": "TX01234",
            },
        ]

        created = 0
        updated = 0
        now = timezone.now()

        with transaction.atomic():
            for entry in customers_data:
                username = entry["username"]
                email = entry.get("email")
                # prepare model fields that actually exist
                defaults = {
                    "password": make_password(entry["password_plain"]),
                    "fullname": entry.get("fullname"),
                    "address": entry.get("address"),
                    "email": email,
                    "phone": entry.get("phone"),
                }

                obj, was_created = Customer.objects.update_or_create(
                    username=username,
                    defaults=defaults
                )

                if was_created:
                    created += 1
                    self.stdout.write(self.style.SUCCESS(f"Created customer: {username}"))
                else:
                    updated += 1
                    self.stdout.write(self.style.WARNING(f"Updated customer: {username} (password reset)"))

                # Log ignored extra fields (for visibility)
                ignored = {k: v for k, v in entry.items() if k not in {"username", "password_plain", "fullname", "address", "email", "phone"}}
                if ignored:
                    self.stdout.write(f"  Ignored extra fields for {username}: {list(ignored.keys())}")

        self.stdout.write(self.style.SUCCESS(f"\nDone. Created: {created}, Updated: {updated}"))
