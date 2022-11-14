from coreapp.tasks import celery_raise_debt
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Raising debt"

    def handle(self, *args, **options):
        celery_raise_debt()
        self.stdout.write("Debt raised successfully!")
