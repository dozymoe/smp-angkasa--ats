"""Django management command to prune old static file cache
"""
from datetime import datetime, timedelta
#-
from django.conf import settings
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    """Prune old static html files
    """
    help = "Prune old static html files."

    def handle(self, *args, **kwargs):
        purge_date = datetime.now() - timedelta(days=7)

        for dest in settings.FROZEN_ROOT.values():
            basepath = settings.ROOT_DIR / dest
            if not basepath.exists():
                continue
            for path in basepath.rglob('*'):
                if path.is_dir():
                    continue
            created_at = datetime.fromtimestamp(path.stat().st_ctime)
            if created_at < purge_date:
                path.unlink()
