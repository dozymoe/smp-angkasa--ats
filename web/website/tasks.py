"""Uwsgi task jobs for website data
"""
from io import BytesIO
import logging
import os
#-
from celery import shared_task
from django.apps import apps
from django.conf import settings
from django.core.files.base import ContentFile
from django.utils import translation
from PIL import Image
#-
from frozen_django.main import generate_static_view
#-
from blog_posting.models import BlogPosting
from my_event.models import Event
from web_page.models import WebPage

_logger = logging.getLogger()


@shared_task
def freeze_view(view_name, host, langcode=None, dest=None, **kwargs):
    """Create static html files cache from Django view
    """
    is_admin = host == settings.ALLOWED_HOSTS[0]
    urlconf = 'web.urls_admin' if is_admin else 'web.urls'
    generate_static_view(view_name, frozen_host=host, frozen_dest=dest,
            langcode=langcode, urlconf=urlconf, **kwargs)


def hosts_freeze_view(view_name, langcode=None, **kwargs):
    """Generate static html files cache for Django view, by hostnames
    """
    for host, dest in settings.FROZEN_ROOT.items():
        freeze_view.delay(view_name, host=host, langcode=langcode,
                dest=str(settings.ROOT_DIR / dest), **kwargs)


def freeze_all_views():
    """Recreate all of the static files cache
    """
    for langcode, _ in settings.LANGUAGES:
        hosts_freeze_view('website.views.Home', langcode=langcode,
                format='html')
        hosts_freeze_view('website.views.EditorHelpText', langcode=langcode,
                format='html')

    for obj in WebPage.objects.filter(published_at__isnull=False,
            deleted_at__isnull=True).all():
        for langcode, _ in settings.LANGUAGES:
            if langcode != obj.valid_language(langcode):
                continue

            with translation.override(langcode):
                hosts_freeze_view('web_page.views.Display', langcode=langcode,
                        slug=obj.slug, format='html')

    for obj in BlogPosting.objects.filter(published_at__isnull=False,
            deleted_at__isnull=True).all():
        for langcode, _ in settings.LANGUAGES:
            if langcode != obj.valid_language(langcode):
                continue

            with translation.override(langcode):
                hosts_freeze_view('blog_posting.views.Display',
                        langcode=langcode, slug=obj.slug, format='html')

    for obj in Event.objects.filter(published_at__isnull=False,
            deleted_at__isnull=True).all():
        for langcode, _ in settings.LANGUAGES:
            if langcode != obj.valid_language(langcode):
                continue

            with translation.override(langcode):
                hosts_freeze_view('my_event.views.Display',
                        langcode=langcode, slug=obj.slug, format='html')


@shared_task
def create_thumbnail(obj_info, source_field, target_field, estimate_size):
    """Create low resolution images for image fields
    """
    model = apps.get_model(obj_info[0], obj_info[1])
    obj = model.objects.get(pk=obj_info[2])

    source = getattr(obj, source_field)
    img = Image.open(source)
    img.load()

    if img.size[0] <= estimate_size[0] and img.size[1] <= estimate_size[1]:
        setattr(obj, target_field, None)
    else:
        img.thumbnail(estimate_size)
        temp_io = BytesIO()
        img.save(temp_io, img.format)

        target = getattr(obj, target_field)
        target.save(os.path.basename(source.name),
                ContentFile(temp_io.getvalue()), save=False)
        # Don't close the image
        #img.close()

    obj.save(update_fields=[target_field])
