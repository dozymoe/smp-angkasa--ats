"""Django signal handlers, see apps.py
"""
from django.conf import settings
#-
from website.tasks import hosts_freeze_view

def front_updated(sender, instance, **kwargs):
    """On front content change, update home page static file
    """
    for langcode, _ in settings.LANGUAGES:
        hosts_freeze_view('website.views.Home', langcode=langcode,
                format='html')


def front_deleted(sender, instance, **kwargs):
    """On front content delete, update home page static file
    """
    for langcode, _ in settings.LANGUAGES:
        hosts_freeze_view('website.views.Home', langcode=langcode,
                format='html')
