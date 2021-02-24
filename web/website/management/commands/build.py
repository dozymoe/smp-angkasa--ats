from django.core.management.base import BaseCommand
#-
from website.tasks import freeze_all_views


class Command(BaseCommand):
    help = "Build static html files."

    def handle(self, *args, **kwargs):
        freeze_all_views()
