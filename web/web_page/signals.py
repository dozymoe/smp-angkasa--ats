from django.conf import settings
from django.utils import translation
#-
from website.tasks import hosts_freeze_view

def post_updated(sender, instance, **kwargs):
    dirty = instance.get_dirty_fields()

    if instance.is_published() or 'published_at' in dirty or\
            'deleted_at' in dirty:

        for langcode, _ in settings.LANGUAGES:
            hosts_freeze_view('website.views.Home', langcode=langcode,
                    format='html')

            if langcode != instance.valid_language(langcode):
                continue

            with translation.override(langcode):
                hosts_freeze_view('web_page.views.Display', langcode=langcode,
                        slug=instance.slug, format='html')


def post_deleted(sender, instance, **kwargs):
    if instance.is_published():
        for langcode, _ in settings.LANGUAGES:
            hosts_freeze_view('website.views.Home', langcode=langcode,
                    format='html')
