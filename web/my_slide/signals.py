"""Django signal handlers, see apps.py
"""
from django.conf import settings
#-
from website.tasks import hosts_freeze_view

def slide_updated(sender, instance, **kwargs):
    """On even change, update home page static file
    """
    for langcode, _ in settings.LANGUAGES:
        hosts_freeze_view('website.views.Home', langcode=langcode,
                format='html')


def slide_deleted(sender, instance, **kwargs):
    """On even delete, update home page static file
    """
    for langcode, _ in settings.LANGUAGES:
        hosts_freeze_view('website.views.Home', langcode=langcode,
                format='html')
