from django.core.management.base import BaseCommand
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from contracts.models import Contracts

class Command(BaseCommand):
    help = 'Expire contracts that have reached their end date and update their status to Inactived.'

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        updated_count = 0

        contracts = Contracts.objects.filter(status='Actived')

        for contract in contracts:
            if contract.start_date and contract.duration:
                end_date = contract.start_date + relativedelta(months=contract.duration.months)
                
                if end_date < today:
                    contract.status = 'Inactived'
                    contract.save(update_fields=['status'])
                    updated_count += 1

        self.stdout.write(self.style.SUCCESS(
            f'✅ Updated {updated_count} contracts from Actived to Inactived.'
        ))
