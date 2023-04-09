"""Django app configuration
"""
from django.apps import AppConfig
from django.db.models.signals import post_save, post_delete
from docutils.parsers.rst import roles

class WebPageConfig(AppConfig):
    """Default app configuration
    """
    name = 'web_page'

    def ready(self):
        # pylint:disable=import-outside-toplevel
        from . import models
        from .restructured_text.embed_page import embed_page_role
        from .signals import page_updated, page_deleted

        post_save.connect(page_updated, sender=models.WebPage,
                dispatch_uid='webpage_save')
        post_delete.connect(page_deleted, sender=models.WebPage,
                dispatch_uid='webpage_delete')

        roles.register_local_role('webpage', embed_page_role)
