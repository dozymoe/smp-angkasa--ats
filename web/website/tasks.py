from io import BytesIO
import logging
import os
#-
from background_task import background
from django.apps import apps
from django.conf import settings
from django.core.files.base import ContentFile
from frozen_django.main import generate_static_view
from PIL import Image
#-
from blog_posting.models import BlogPosting
from web_page.models import WebPage

_logger = logging.getLogger()


@background(schedule={'priority': 0})
def freeze_view(view_name, base_url, dest=None, **kwargs):
    generate_static_view(view_name, frozen_host=base_url, frozen_dest=dest,
            **kwargs)


def hosts_freeze_view(view_name, dest=None, **kwargs):
    host = settings.ALLOWED_HOSTS[0]
    freeze_view(view_name, base_url=host, dest=dest, **kwargs)


def freeze_all_views():
    hosts_freeze_view('website.views.Home', format='html')
    hosts_freeze_view('website.views.EditorHelpText', format='html')

    for obj in BlogPosting.objects.filter(published_at__isnull=False,
            deleted_at__isnull=True).all():
        hosts_freeze_view('blog_posting.views.Display', slug=obj.slug,
                format='html')

    for obj in WebPage.objects.filter(published_at__isnull=False,
            deleted_at__isnull=True).all():
        hosts_freeze_view('web_page.views.Display', slug=obj.slug,
                format='html')


@background(schedule={'priority': 3})
def create_thumbnail(obj_info, source_field, target_field, estimate_size):
    model = apps.get_model(obj_info[0], obj_info[1])
    obj = model.objects.get(pk=obj_info[2])

    source = getattr(obj, source_field)
    im = Image.open(source)
    im.load()

    if im.size[0] <= estimate_size[0] and im.size[1] <= estimate_size[1]:
        setattr(obj, target_field, None)
    else:
        im.thumbnail(estimate_size, Image.ANTIALIAS)
        io = BytesIO()
        im.save(io, im.format)

        target = getattr(obj, target_field)
        target.save(os.path.basename(source.name), ContentFile(io.getvalue()),
                save=False)
        # Don't close the image
        #im.close()

    obj.save(update_fields=[target_field])
