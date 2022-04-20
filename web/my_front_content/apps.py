from django.apps import AppConfig
from django.db.models.signals import post_save, post_delete

class MyFrontContentConfig(AppConfig):
    name = 'my_front_content'

    def ready(self):
        # pylint:disable=import-outside-toplevel
        from . import models
        from .signals import post_updated, post_deleted

        post_save.connect(post_updated, sender=models.FrontContent)
        post_delete.connect(post_deleted, sender=models.FrontContent)
