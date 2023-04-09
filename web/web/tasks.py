"""Uwsgi task workers entry point
"""
from uwsgi_tasks import django_setup, set_uwsgi_callbacks

set_uwsgi_callbacks()
django_setup()
