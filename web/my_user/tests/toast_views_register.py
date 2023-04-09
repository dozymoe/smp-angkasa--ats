"""Django integration tests for my_user
"""
import logging
#-
from django.test import TestCase
#-
from my_user.models import User

_logger = logging.getLogger(__name__)


class RegisterTest(TestCase):
    """Test registration page
    """
    @classmethod
    def setUpTestData(cls):
        # Create User
        cls.user = User.objects.create_user(username='user', password='12345')


    def test_get_anon(self):
        """When anon user accesses the page
        """
        response = self.client.get('/account/signup/')
        self.assertEqual(response.status_code, 200)


    def test_get(self):
        """When authenticated user accesses the page
        """
        # Login
        login = self.client.login(username='user', password='12345')
        self.assertTrue(login)
        # Home view
        response = self.client.get('/account/signup/')
        self.assertRedirects(response, '/companies/index.html')
