from django.apps import AppConfig
from django.db.models.signals import post_save, post_delete
from docutils.parsers.rst import roles


class BlogPostingConfig(AppConfig):
    name = 'blog_posting'

    def ready(self):
        # pylint:disable=import-outside-toplevel
        from . import models
        from .restructured_text.embed_blog import embed_blog_role
        from .signals import post_updated, post_deleted

        post_save.connect(post_updated, sender=models.BlogPosting)
        post_delete.connect(post_deleted, sender=models.BlogPosting)

        roles.register_local_role('webblog', embed_blog_role)
