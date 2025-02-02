"""Django integration tests for my_user
"""
import logging
#-
from yarl import URL
#-
from web.testcases.testcase import SmpTestCase

_logger = logging.getLogger(__name__)

class LoginTest(SmpTestCase):
    """Test login page
    """
    LOGIN_URL = URL('/account/login/')
    ADMIN_LOGIN_URL = URL('/admin/login/')

    def test_get_anon(self):
        """When anon user accesses the page
        """
        resp = self.client.get(self.LOGIN_URL, **self.client_env(admin=False))
        self.assertEqual(resp.status_code, 404)

        resp = self.client.get(self.LOGIN_URL, **self.client_env(admin=True))
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get(self.ADMIN_LOGIN_URL, **self.client_env(admin=False))
        self.assertEqual(resp.status_code, 404)

        resp = self.client.get(self.ADMIN_LOGIN_URL, **self.client_env(admin=True))
        self.assertEqual(resp.status_code, 200)


    def test_post_banned(self):
        """When authenticated user accesses the page
        """
        resp = self.client.post(self.LOGIN_URL,
                {
                    'login': self.BANNED1_USERNAME,
                    'password': self.BANNED1_PASSWORD,
                },
                **self.client_env(admin=False))
        self.assertEqual(resp.status_code, 404)

        resp = self.client.post(self.LOGIN_URL,
                {
                    'login': self.BANNED1_USERNAME,
                    'password': self.BANNED1_PASSWORD,
                },
                **self.client_env(admin=True))
        self.assertNoFormErrors(resp)
        self.assertEqual(resp.status_code, 200)
        self.client.logout()

        resp = self.client.post(self.ADMIN_LOGIN_URL,
                {
                    'username': self.BANNED1_USERNAME,
                    'password': self.BANNED1_PASSWORD,
                },
                **self.client_env(admin=True))
        self.assertNoFormErrors(resp)
        self.assertEqual(resp.status_code, 200)

        url = self.ADMIN_URL / 'blog_posting/blogposting/'
        resp = self.client.get(url, **self.client_env(admin=True))
        self.assertRedirects(resp,
                self.ADMIN_LOGIN_URL % {'next': str(url)},
                status_code=302, target_status_code=200,
                fetch_redirect_response=True)


    def test_post_user(self):
        """When authenticated user accesses the page
        """
        resp = self.client.post(self.LOGIN_URL,
                {
                    'login': self.USER1_USERNAME,
                    'password': self.USER1_PASSWORD,
                },
                **self.client_env(admin=False))
        self.assertEqual(resp.status_code, 404)

        resp = self.client.post(self.LOGIN_URL,
                {
                    'login': self.USER1_USERNAME,
                    'password': self.USER1_PASSWORD,
                },
                **self.client_env(admin=True))
        self.assertNoFormErrors(resp)
        self.assertEqual(resp.status_code, 200)
        self.client.logout()

        resp = self.client.post(self.ADMIN_LOGIN_URL,
                {
                    'username': self.USER1_USERNAME,
                    'password': self.USER1_PASSWORD,
                },
                **self.client_env(admin=True))
        self.assertNoFormErrors(resp)
        self.assertEqual(resp.status_code, 200)

        url = self.ADMIN_URL / 'blog_posting/blogposting/'
        resp = self.client.get(url, **self.client_env(admin=True))
        self.assertRedirects(resp,
                self.ADMIN_LOGIN_URL % {'next': str(url)},
                status_code=302, target_status_code=200,
                fetch_redirect_response=True)


    def test_post_staff(self):
        """When staff accesses the page
        """
        resp = self.client.post(self.LOGIN_URL,
                {
                    'login': self.STAFF1_USERNAME,
                    'password': self.STAFF1_PASSWORD,
                },
                **self.client_env(admin=False))
        self.assertEqual(resp.status_code, 404)

        resp = self.client.post(self.LOGIN_URL,
                {
                    'login': self.STAFF1_USERNAME,
                    'password': self.STAFF1_PASSWORD,
                },
                **self.client_env(admin=True))
        self.assertNoFormErrors(resp)
        self.assertRedirects(resp,
                '/',
                status_code=302, target_status_code=200,
                fetch_redirect_response=True)
        self.client.logout()

        resp = self.client.post(self.ADMIN_LOGIN_URL,
                {
                    'username': self.STAFF1_USERNAME,
                    'password': self.STAFF1_PASSWORD,
                },
                **self.client_env(admin=True))
        self.assertNoFormErrors(resp)
        self.assertRedirects(resp, '/',
                status_code=302, target_status_code=200,
                fetch_redirect_response=True)

        url = self.ADMIN_URL / 'blog_posting/blogposting/'
        resp = self.client.get(url, **self.client_env(admin=True))
        self.assertRedirects(resp,
                self.ADMIN_LOGIN_URL % {'next': str(url)},
                status_code=302, target_status_code=200,
                fetch_redirect_response=True)


    def test_post_admin(self):
        """When admin accesses the page
        """
        resp = self.client.post(self.LOGIN_URL,
                {
                    'login': self.ADMIN1_USERNAME,
                    'password': self.ADMIN1_PASSWORD,
                },
                **self.client_env(admin=False))
        self.assertEqual(resp.status_code, 404)

        resp = self.client.post(self.LOGIN_URL,
                {
                    'login': self.ADMIN1_USERNAME,
                    'password': self.ADMIN1_PASSWORD,
                },
                **self.client_env(admin=True))
        self.assertNoFormErrors(resp)
        self.assertRedirects(resp,
                '/',
                status_code=302, target_status_code=200,
                fetch_redirect_response=True)
        self.client.logout()

        resp = self.client.post(self.ADMIN_LOGIN_URL,
                {
                    'username': self.ADMIN1_USERNAME,
                    'password': self.ADMIN1_PASSWORD,
                },
                **self.client_env(admin=True))
        self.assertNoFormErrors(resp)
        self.assertEqual(resp.status_code, 200)

        url = self.ADMIN_URL / 'blog_posting/blogposting/'
        resp = self.client.get(url, **self.client_env(admin=True))
        self.assertRedirects(resp,
                self.ADMIN_LOGIN_URL % {'next': str(url)},
                status_code=302, target_status_code=200,
                fetch_redirect_response=True)
