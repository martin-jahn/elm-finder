
from django.core.management.base import BaseCommand


from apps.searchv2.tasks import build_index
class Command(BaseCommand):

    help = "Constructs the search results for the system"

    def handle(self, *args, **options):
        build_index.delay()
