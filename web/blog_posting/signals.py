"""Django signal handlers, see apps.py
"""
from django.conf import settings
from django.utils import translation
#-
from website.tasks import hosts_freeze_view

def blog_updated(sender, instance, **kwargs):
    """On blog post change, rebuild static files and low resolution images
    """
    dirty = instance.get_dirty_fields()

    if instance.is_published() or 'published_at' in dirty or\
            'deleted_at' in dirty:

        for langcode, _ in settings.LANGUAGES:
            hosts_freeze_view('website.views.Home', langcode=langcode,
                    format='html')

            if langcode != instance.valid_language(langcode):
                continue

            with translation.override(langcode):
                hosts_freeze_view('blog_posting.views.Display',
                        langcode=langcode, slug=instance.slug, format='html')


def blog_deleted(sender, instance, **kwargs):
    """On blog post delete, update home page static file
    """
    if instance.is_published():
        for langcode, _ in settings.LANGUAGES:
            hosts_freeze_view('website.views.Home', langcode=langcode,
                    format='html')
