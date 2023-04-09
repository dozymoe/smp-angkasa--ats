"""Django management command to rebuild static file cache
"""
from django.core.management.base import BaseCommand
#-
from website.tasks import freeze_all_views

class Command(BaseCommand):
    """Build static html files
    """
    help = "Build static html files."

    def handle(self, *args, **kwargs):
        freeze_all_views()
