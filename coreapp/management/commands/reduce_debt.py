from coreapp.tasks import celery_reduce_debt
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Reducing debt"

    def handle(self, *args, **options):
        celery_reduce_debt()
        self.stdout.write("Debt reduced successfully!")
