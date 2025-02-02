"""Create shared sites for integration tests
"""
from django.conf import settings
from django.contrib.sites.models import Site

def create_test_sites(sender, **kwargs):
    """Create test sites
    """
    # This is set in DiscoveryRunner
    if not settings.TESTING:
        return

    for ii, hostname in enumerate(settings.ALLOWED_HOSTS):
        Site.objects.update_or_create(
            domain=hostname,
            defaults={
                'name': f'NormalSite{ii}' if ii else 'AdminSite',
            }
        )
