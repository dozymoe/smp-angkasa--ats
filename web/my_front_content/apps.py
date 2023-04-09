"""Django app configuration
"""
from django.apps import AppConfig
from django.db.models.signals import post_save, post_delete

class MyFrontContentConfig(AppConfig):
    """Default app configuration
    """
    name = 'my_front_content'

    def ready(self):
        # pylint:disable=import-outside-toplevel
        from . import models
        from .signals import front_updated, front_deleted

        post_save.connect(front_updated, sender=models.FrontContent,
                dispatch_uid='myfrontcontent_save')
        post_delete.connect(front_deleted, sender=models.FrontContent,
                dispatch_uid='myfrontcontent_delete')
