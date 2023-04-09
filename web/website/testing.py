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

    # Replace default site with Admin site first
    Site.objects.update_or_create(
            id=1,
            defaults={
                'domain': settings.ALLOWED_HOSTS[0],
                'name': "Manage Testing Site",
            })
    # Add normal visitor site
    Site.objects.update_or_create(
            id=2,
            defaults={
                'domain': settings.ALLOWED_HOSTS[1],
                'name': "Testing Site",
            })
