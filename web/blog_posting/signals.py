from django.conf import settings
#-
from website.tasks import create_thumbnail, hosts_freeze_view


def post_updated(sender, instance, **kwargs):
    dirty = instance.get_dirty_fields()

    # Ignore thumbnail images.
    for field, _, _ in settings.IMAGE_SIZES:
        if field in dirty:
            return

    if 'image' in dirty and bool(instance.image):
        for field, size, _ in settings.IMAGE_SIZES:
            create_thumbnail(
                    ('blog_posting', 'BlogPosting', instance.pk),
                    'image', field, size)

    hosts_freeze_view('website.views.Home', format='html')
    hosts_freeze_view('blog_posting.views.Display', slug=instance.slug,
            format='html')


def post_deleted(sender, instance, **kwargs):
    hosts_freeze_view('website.views.Home', format='html')
