import logging
#-
from django.test import TestCase
#-
from myuser.models import User

_logger = logging.getLogger(__name__)


class LoginTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create User
        cls.user = User.objects.create_user(username='user', password='12345')


    def test_get_anon(self):
        response = self.client.get('/account/login/')
        self.assertEqual(response.status_code, 200)


    def test_get(self):
        # Login
        login = self.client.login(username='user', password='12345')
        self.assertTrue(login)
        # Home view
        response = self.client.get('/account/login/')
        self.assertRedirects(response, '/companies/index.html')
