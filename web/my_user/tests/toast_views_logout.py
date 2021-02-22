import logging
#-
from django.test import TestCase
#-
from my_user.models import User

_logger = logging.getLogger(__name__)


class LogoutTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create User
        cls.user = User.objects.create_user(username='user', password='12345')


    def test_get_anon(self):
        response = self.client.get('/account/logout/')
        self.assertRedirects(response, '/')


    def test_get(self):
        # Login
        login = self.client.login(username='user', password='12345')
        self.assertTrue(login)
        # Home view
        response = self.client.get('/account/logout/')
        self.assertRedirects(response, '/')
