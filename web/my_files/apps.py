"""Django app configuration
"""
from django.apps import AppConfig
from django.db.models.signals import pre_save, post_delete, post_save
from docutils.parsers.rst import directives, roles

class MyFilesConfig(AppConfig):
    """Default app configuration
    """
    name = 'my_files'

    def ready(self):
        # pylint:disable=import-outside-toplevel
        from . import models
        from .restructured_text.embed_file import EmbedFileDirective
        from .restructured_text.embed_file import embed_file_role
        from .signals import file_deleted, file_updating, file_updated

        pre_save.connect(file_updating, sender=models.MyFile,
                dispatch_uid='myfiles_presave')
        post_save.connect(file_updated, sender=models.MyFile,
                dispatch_uid='myfiles_save')
        post_delete.connect(file_deleted, sender=models.MyFile,
                dispatch_uid='myfiles_delete')

        directives.register_directive('webfile', EmbedFileDirective)
        roles.register_local_role('webfile', embed_file_role)
