"""Django integration tests for my_user
"""
import logging
#-
from yarl import URL
#-
from web.testcases.testcase import SmpTestCase

_logger = logging.getLogger(__name__)

class RegisterTest(SmpTestCase):
    """Test registration page
    """
    SIGNUP_URL = URL('/account/signup/')

    def test_get_anon(self):
        """When anon user accesses the page
        """
        resp = self.client.get(self.SIGNUP_URL, **self.client_env(admin=False))
        self.assertEqual(resp.status_code, 404)

        resp = self.client.get(self.SIGNUP_URL, **self.client_env(admin=True))
        self.assertContains(resp, 'ditutup', status_code=200)
