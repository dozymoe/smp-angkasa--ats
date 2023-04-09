"""Test the management pages for files
"""
from yarl import URL
#-
from web.testcases.testcase import SmpTestCase

class TestManageFileIndexPage(SmpTestCase):
    """Test administration page for listing files
    """
    def test_anon_get(self):
        """When anon user access admin file list
        """
        base_url = URL('/files')

        resp = self.client.get(base_url / '',
                **self.client_env(admin=True))
        self.assertRedirects(resp,
                URL('/account/login/') % {'next': '/files/'}, 302,
                target_status_code=200, fetch_redirect_response=True)


    def test_user_get(self):
        """When authenticated user access admin file list
        """
        base_url = URL('/files')

        self.login_user01()

        resp = self.client.get(base_url / '',
                **self.client_env(admin=True))
        self.assertEqual(resp.status_code, 200)
