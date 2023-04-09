"""Test the management pages for files
"""
from django.test import SimpleTestCase
from django.urls import reverse
from yarl import URL
#-
from web import urls_admin

class TestManageFileRoutes(SimpleTestCase):
    """Test administration routing for files
    """
    def test_routes(self):
        """Check reverse routes are correct
        """
        base_url = URL('/files')

        self.assertEqual(reverse('MyFile:Index', urls_admin),
                str(base_url / ''))
        self.assertEqual(reverse('MyFile:Create', urls_admin),
                str(base_url / 'add'))
        self.assertEqual(reverse('MyFile:Update', urls_admin, (123,)),
                str(base_url / '123/edit'))
        self.assertEqual(reverse('MyFile:Destroy', urls_admin, (123,)),
                str(base_url / '123/delete'))
