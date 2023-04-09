"""Django app configuration
"""
from django.apps import AppConfig
from django.db.models.signals import post_save, post_delete
from docutils.parsers.rst import roles

class MyEventConfig(AppConfig):
    """Default app configuration
    """
    name = 'my_event'

    def ready(self):
        # pylint:disable=import-outside-toplevel
        from . import models
        from .restructured_text.embed_event import embed_event_role
        from .signals import event_updated, event_deleted

        post_save.connect(event_updated, sender=models.Event,
                dispatch_uid='myevent_save')
        post_delete.connect(event_deleted, sender=models.Event,
                dispatch_uid='myevent_delete')

        roles.register_local_role('webevent', embed_event_role)
