from website.tasks import hosts_freeze_view


def post_updated(sender, instance, **kwargs):
    hosts_freeze_view('website.views.Home', format='html')
    hosts_freeze_view('web_page.views.Display', slug=instance.slug,
            format='html')


def post_deleted(sender, instance, **kwargs):
    hosts_freeze_view('website.views.Home', format='html')
