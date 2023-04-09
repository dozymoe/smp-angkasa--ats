"""Django management command for deleting old website assets
"""
import json
import os
from pathlib import Path
#-
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    """Cleanup old css and js assets
    """
    help = "Cleanup old css and js assets."

    def handle(self, *args, **kwargs):
        project = os.environ['PROJECT_NAME']
        rootdir = Path(os.environ['ROOT_DIR']).resolve(strict=True)
        public_dir = rootdir/project/'static'

        metafile = rootdir/'var'/project/'webpack-css.meta.json'
        if metafile.exists():
            with open(metafile, 'r', encoding='utf-8') as f:
                meta = json.load(f)
                filenames = [os.path.basename(x) for x in meta.values()]

            assets_dir = public_dir/'css'
            for filename in os.listdir(assets_dir):
                if filename in ('.', '..'):
                    continue
                if filename in filenames:
                    continue
                filename = os.path.join(assets_dir, filename)
                os.remove(filename)

        metafile = rootdir/'var'/project/'webpack-js.meta.json'
        if metafile.exists():
            with open(metafile, 'r', encoding='utf-8') as f:
                meta = json.load(f)
                filenames = [os.path.basename(x) for x in meta.values()]

            assets_dir = public_dir/'js'
            for filename in os.listdir(assets_dir):
                if filename in ('.', '..'):
                    continue
                if filename in filenames:
                    continue
                filename = os.path.join(assets_dir, filename)
                os.remove(filename)

        self.stdout.write(self.style.SUCCESS("css and js files cleaned."))
