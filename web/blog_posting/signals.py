from website.tasks import create_thumbnail, hosts_freeze_view
from .models import COVER_SIZE


def post_updated(sender, instance, **kwargs):
    dirty = instance.get_dirty_fields()
    if 'image' in dirty and bool(instance.image) and\
            ('cover' not in dirty or not bool(instance.cover)):
        create_thumbnail(
                ('blog_posting', 'BlogPosting', instance.pk),
                'image', 'cover', COVER_SIZE)
        # Will be triggered again by creating cover image, quit for now.
        return

    hosts_freeze_view('website.views.Home', format='html')
    hosts_freeze_view('blog_posting.views.Display', slug=instance.slug,
            format='html')


def post_deleted(sender, instance, **kwargs):
    hosts_freeze_view('website.views.Home', format='html')
