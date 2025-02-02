"""Django test runner that separate UnitTest and IntegrationTest
"""
import logging
import os
from unittest.suite import TestSuite
#-
from django.conf import settings
from django.test import TransactionTestCase
from django.test.runner import DiscoverRunner

_logger = logging.getLogger()

class IntegrationTestRunner(DiscoverRunner):
    """Only run integration tests
    """
    def build_suite(self, *args, **kwargs):
        # Customize Django settings for testing
        settings.DEBUG = False
        settings.TESTING = True
        settings.PASSWORD_HASHERS = [
            'django.contrib.auth.hashers.MD5PasswordHasher',
        ]
        settings.MEDIA_ROOT = str(settings.MEDIA_ROOT) + '_test'
        os.makedirs(settings.MEDIA_ROOT, exist_ok=True)

        suite = super().build_suite(*args, **kwargs)
        tests = [t for t in suite._tests if self.filter(t)] # pylint:disable=protected-access
        return TestSuite(tests=tests)


    def filter(self, test):
        """Filter running test cases
        """
        return issubclass(test.__class__, TransactionTestCase)


class UnitTestRunner(DiscoverRunner):
    """Only run unit tests
    """
    def setup_databases(self, **kwargs):
        pass


    def teardown_databases(self, old_config, **kwargs):
        pass


    def build_suite(self, *args, **kwargs):
        suite = super().build_suite(*args, **kwargs)
        tests = [t for t in suite._tests if self.filter(t)] # pylint:disable=protected-access
        return TestSuite(tests=tests)


    def filter(self, test):
        """Filter running test cases
        """
        return not issubclass(test.__class__, TransactionTestCase)
