"""Django app configuration
"""
from django.apps import AppConfig
from django.db.models.signals import post_save, post_delete
from docutils.parsers.rst import roles

class BlogPostingConfig(AppConfig):
    """Default app configuration
    """
    name = 'blog_posting'

    def ready(self):
        # pylint:disable=import-outside-toplevel
        from . import models
        from .restructured_text.embed_blog import embed_blog_role
        from .signals import blog_updated, blog_deleted

        post_save.connect(blog_updated, sender=models.BlogPosting,
                dispatch_uid='blogposting_save')
        post_delete.connect(blog_deleted, sender=models.BlogPosting,
                dispatch_uid='blogposting_delete')

        roles.register_local_role('webblog', embed_blog_role)
