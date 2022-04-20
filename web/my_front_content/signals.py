from django.conf import settings
#-
from website.tasks import hosts_freeze_view

def post_updated(sender, instance, **kwargs):
    for langcode, _ in settings.LANGUAGES:
        hosts_freeze_view('website.views.Home', langcode=langcode,
                format='html')


def post_deleted(sender, instance, **kwargs):
    for langcode, _ in settings.LANGUAGES:
        hosts_freeze_view('website.views.Home', langcode=langcode,
                format='html')
