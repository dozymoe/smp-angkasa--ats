import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_FILES = [
    "etc/production/logging.json",
    "etc/production/web/account.json",
    "etc/production/web/application.json",
    "etc/production/web/database.json",
    "etc/production/web/server.json"
]
PYTHON_PATHS = [
    "lib-py/django-materialweb",
    "lib-py/frozen-django"
]

os.environ['ROOT_DIR'] = ROOT_DIR
os.environ['PROJECT_NAME'] = 'web'
os.environ['PROJECT_VARIANT'] = 'production'
os.environ['CONFIG_FILENAMES'] = os.pathsep.join(os.path.join(ROOT_DIR, x)\
        for x in CONFIG_FILES)
for path in PYTHON_PATHS:
    sys.path.insert(0, os.path.join(ROOT_DIR, path))

from web.wsgi import application
