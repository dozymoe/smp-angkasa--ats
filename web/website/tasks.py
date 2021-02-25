from background_task import background
from django.conf import settings
from frozen_django.main import generate_static_view

@background(schedule=60)
def freeze_view(view_name, base_url, dest=None, **kwargs):
    generate_static_view(view_name, frozen_host=base_url, frozen_dest=dest,
            **kwargs)


def hosts_freeze_view(view_name, dest=None, **kwargs):
    host = settings.ALLOWED_HOSTS[0]
    freeze_view(view_name, base_url=host, dest=dest, **kwargs)


def freeze_all_views():
    hosts_freeze_view('website.views.Home', format='html')
    hosts_freeze_view('website.views.VisiMisi', format='html')
    hosts_freeze_view('website.views.Ppdb', format='html')
