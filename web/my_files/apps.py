from django.apps import AppConfig
from django.db.models.signals import pre_save, post_save
from docutils.parsers.rst import directives


class MyFilesConfig(AppConfig):
    name = 'my_files'

    def ready(self):
        # pylint:disable=import-outside-toplevel
        from . import models
        from .restructured_text.embed_file import EmbedFileDirective
        from .signals import file_updating, file_updated

        pre_save.connect(file_updating, sender=models.MyFile)
        post_save.connect(file_updated, sender=models.MyFile)

        directives.register_directive('embed_file', EmbedFileDirective)
