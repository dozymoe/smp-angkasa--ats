from django.apps import AppConfig
from django.db.models.signals import post_save, post_delete
from docutils.parsers.rst import roles

class MyEventConfig(AppConfig):
    name = 'my_event'

    def ready(self):
        # pylint:disable=import-outside-toplevel
        from . import models
        from .restructured_text.embed_event import embed_event_role
        from .signals import post_updated, post_deleted

        post_save.connect(post_updated, sender=models.Event)
        post_delete.connect(post_deleted, sender=models.Event)

        roles.register_local_role('webevent', embed_event_role)
