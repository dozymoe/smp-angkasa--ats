"""Test the web pages that serves files
"""
import logging
#-
from django.test import SimpleTestCase
from django.urls import reverse
from yarl import URL
#-
from web import urls
from web.testcases.testcase import SmpTestCase

_logger = logging.getLogger(__name__)


class TestFileRoutes(SimpleTestCase):
    """Test routing for working with files
    """
    def test_routes(self):
        """Check reverse routes are correct for Indonesia
        """
        base_url = URL('/files')

        self.assertEqual(reverse('MyFile:Display', urls, (123,)),
                str(base_url / '123/view'))
        self.assertEqual(reverse('MyFile:Display', urls, (123, 'xs')),
                str(base_url / '123/view-xs'))


class TestFileDisplayPage(SmpTestCase):
    """Test web pages for files
    """
    def test_anon_get_notfound(self):
        """When anon user access wrong file for Indonesia
        """
        base_url = URL('/files')

        resp = self.client.get(base_url / '32767/view',
                **self.client_env(admin=False))
        self.assertEqual(resp.status_code, 404)
