from django.apps import AppConfig
from django.db.models.signals import post_save
from docutils.parsers.rst import directives


class WebPageConfig(AppConfig):
    name = 'web_page'

    def ready(self):
        # pylint:disable=import-outside-toplevel
        from . import models
        from .restructured_text.embed_page import EmbedPageDirective
        from .signals import post_updated

        post_save.connect(post_updated, sender=models.WebPage)

        directives.register_directive('webpage', EmbedPageDirective)
