from django.apps import AppConfig
from docutils.parsers.rst import roles


class MyEventConfig(AppConfig):
    name = 'my_event'

    def ready(self):
        # pylint:disable=import-outside-toplevel
        from .restructured_text.embed_event import embed_event_role

        roles.register_local_role('webevent', embed_event_role)
