import logging
import os
from pathlib import Path
import re
import subprocess
#-
from django.core.management.base import BaseCommand

_logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Cleanup translation message that only updated their timestamps."

    FILE_COUNT_PATTERN = re.compile(r'\b(?P<num>\d+)\sfile\b')
    INSERT_COUNT_PATTERN = re.compile(r'\b(?P<num>\d+)\sinsertions\b')
    DELETE_COUNT_PATTERN = re.compile(r'\b(?P<num>\d+)\sdeletions\b')

    def handle(self, *args, **kwargs):
        rootdir = Path(os.environ['ROOT_DIR'])
        out = subprocess.check_output(['git', 'diff', '--name-only'],
                cwd=rootdir).decode()
        for filename in out.splitlines():
            if not filename.endswith('.po'):
                continue
            out = subprocess.check_output(['git', 'diff', '--shortstat',
                    filename],
                    cwd=rootdir).decode()
            #_logger.debug(out)
            match = self.FILE_COUNT_PATTERN.search(out)
            if match:
                numfile = int(match.group('num'))
            else:
                numfile = 0
            match = self.INSERT_COUNT_PATTERN.search(out)
            if match:
                insert = int(match.group('num'))
            else:
                insert = 0
            match = self.DELETE_COUNT_PATTERN.search(out)
            if match:
                delete = int(match.group('num'))
            else:
                delete = 0

            if numfile <= 1 and insert <= 1 and delete <= 1:
                subprocess.check_call(['git', 'checkout', filename],
                        cwd=rootdir)
