from django.apps import AppConfig
from docutils.parsers.rst import directives


class WebsiteConfig(AppConfig):
    name = 'website'

    def ready(self):
        # pylint:disable=import-outside-toplevel
        from .restructured_text.embed_youtube import EmbedYoutubeDirective

        directives.register_directive('youtube', EmbedYoutubeDirective)
