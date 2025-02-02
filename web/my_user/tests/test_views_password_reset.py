"""Django integration tests for my_user
"""
import logging
#-
from yarl import URL
#-
from web.testcases.testcase import SmpTestCase

_logger = logging.getLogger(__name__)

class PasswordResetTest(SmpTestCase):
    """Test password reset page
    """
    RESET_URL = URL('/account/password/reset/')

    def test_get_anon(self):
        """When anon user accesses the page
        """
        resp = self.client.get(self.RESET_URL, **self.client_env(admin=False))
        self.assertEqual(resp.status_code, 404)

        resp = self.client.get(self.RESET_URL, **self.client_env(admin=True))
        self.assertEqual(resp.status_code, 200)


    def test_get(self):
        """When authenticated user accesses the page
        """
        self.login_user1()
        resp = self.client.get(self.RESET_URL, **self.client_env(admin=False))
        self.assertEqual(resp.status_code, 404)

        resp = self.client.get(self.RESET_URL, **self.client_env(admin=True))
        self.assertEqual(resp.status_code, 200)
