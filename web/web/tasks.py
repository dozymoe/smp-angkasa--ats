#pylint:disable=wrong-import-position,unused-import
from uwsgi_tasks import django_setup, set_uwsgi_callbacks

set_uwsgi_callbacks()
django_setup()
