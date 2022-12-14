from coreapp.services import fill_db
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Filling DB with test data"

    def handle(self, *args, **options):
        fill_db()
        self.stdout.write("Successfully added test data to DB!")
