"""Django app configuration
"""
from django.apps import AppConfig
from django.db.models.signals import post_save, post_delete

class MySlideConfig(AppConfig):
    """Default app configuration
    """
    name = 'my_slide'

    def ready(self):
        # pylint:disable=import-outside-toplevel
        from . import models
        from .signals import slide_updated, slide_deleted

        post_save.connect(slide_updated, sender=models.MySlide,
                dispatch_uid='myslide_save')
        post_delete.connect(slide_deleted, sender=models.MySlide,
                dispatch_uid='myslide_delete')
