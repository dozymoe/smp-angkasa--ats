"""Django app configuration
"""
from django.apps import AppConfig
from django.db.models.signals import post_migrate
from docutils.parsers.rst import directives

class WebsiteConfig(AppConfig):
    """Default app configuration
    """
    name = 'website'

    def ready(self):
        # pylint:disable=import-outside-toplevel
        from .restructured_text.embed_youtube import EmbedYoutubeDirective
        from .testing import create_test_sites

        # For testing
        # Note: will only trigger if models.py exists even if it's empty
        post_migrate.connect(create_test_sites, sender=self,
                dispatch_uid='website_migrate_test_sites')

        directives.register_directive('youtube', EmbedYoutubeDirective)
