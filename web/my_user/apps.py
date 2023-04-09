"""Django app configuration
"""
from django.apps import AppConfig
from django.db.models.signals import post_migrate

class MyUserConfig(AppConfig):
    """Default app configuration
    """
    name = 'my_user'

    def ready(self):
        # pylint:disable=import-outside-toplevel
        from .testing import create_test_users

        # For testing
        post_migrate.connect(create_test_users, sender=self,
                dispatch_uid='myuser_migrate_test_users')
