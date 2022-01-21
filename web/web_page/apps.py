from django.apps import AppConfig
from django.db.models.signals import post_save
from docutils.parsers.rst import roles


class WebPageConfig(AppConfig):
    name = 'web_page'

    def ready(self):
        # pylint:disable=import-outside-toplevel
        from . import models
        from .restructured_text.embed_page import embed_page_role
        from .signals import post_updated

        post_save.connect(post_updated, sender=models.WebPage)

        roles.register_local_role('webpage', embed_page_role)