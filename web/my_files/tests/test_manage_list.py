"""Test the management pages for files
"""
from yarl import URL
#-
from web.testcases.testcase import SmpTestCase

class TestManageFileIndexPage(SmpTestCase):
    """Test administration page for listing files
    """
    BASE_URL = URL('/files/')

    def test_anon_get(self):
        """When anon user access admin file list
        """
        resp = self.client.get(self.BASE_URL,
                **self.client_env(admin=True))
        self.assertRedirects(resp,
                self.LOGIN_URL % {'next': str(self.BASE_URL)},
                302, target_status_code=200, fetch_redirect_response=True)


    def test_user_get(self):
        """When authenticated user access admin file list
        """
        self.login_user1()

        resp = self.client.get(self.BASE_URL,
                **self.client_env(admin=True))
        self.assertEqual(resp.status_code, 200)
