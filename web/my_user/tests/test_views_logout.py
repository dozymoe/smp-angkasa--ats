"""Django integration tests for my_user
"""
import logging
#-
from django.contrib.auth import get_user_model
from yarl import URL
#-
from web.testcases.testcase import SmpTestCase

_logger = logging.getLogger(__name__)

class LogoutTest(SmpTestCase):
    """Test logout page
    """
    LOGOUT_URL = URL('/account/logout/')
    ADMIN_LOGOUT_URL = URL('/admin/logout/')

    def test_get_anon(self):
        """When anon user accesses the page
        """
        resp = self.client.get(self.LOGOUT_URL, **self.client_env(admin=False))
        self.assertEqual(resp.status_code, 404)

        resp = self.client.get(self.LOGOUT_URL, **self.client_env(admin=True))
        self.assertRedirects(resp,
                self.LOGIN_URL,
                status_code=302, target_status_code=200,
                fetch_redirect_response=True)

        resp = self.client.get(self.ADMIN_LOGOUT_URL,
                **self.client_env(admin=False))
        self.assertEqual(resp.status_code, 404)

        resp = self.client.get(self.ADMIN_LOGOUT_URL,
                **self.client_env(admin=True))
        self.assertRedirects(resp,
                self.ADMIN_URL,
                status_code=302, target_status_code=302,
                fetch_redirect_response=True)


    def test_user(self):
        """When authenticated user accesses the page
        """
        self.login_user1()
        resp = self.client.get(self.LOGOUT_URL, **self.client_env(admin=False))
        self.assertEqual(resp.status_code, 404)
        resp = self.client.post(self.LOGOUT_URL, {}, **self.client_env(admin=False))
        self.assertEqual(resp.status_code, 404)

        self.login_user1()
        resp = self.client.get(self.LOGOUT_URL, **self.client_env(admin=True))
        self.assertRedirects(resp,
                self.LOGIN_URL,
                status_code=302, target_status_code=200,
                fetch_redirect_response=True)

        self.login_user1()
        resp = self.client.post(self.LOGOUT_URL, {}, **self.client_env(admin=True))
        self.assertRedirects(resp,
                self.LOGIN_URL,
                status_code=302, target_status_code=200,
                fetch_redirect_response=True)

        self.login_user1()
        resp = self.client.get(self.ADMIN_LOGOUT_URL, **self.client_env(admin=True))
        self.assertRedirects(resp,
                self.ADMIN_URL,
                status_code=302, target_status_code=302,
                fetch_redirect_response=True)

        self.login_user1()
        resp = self.client.post(self.ADMIN_LOGOUT_URL, {},
                **self.client_env(admin=True))
        self.assertRedirects(resp,
                self.ADMIN_URL,
                status_code=302, target_status_code=302,
                fetch_redirect_response=True)


    def test_staff(self):
        """When staff accesses the page
        """
        self.login_staff1()
        resp = self.client.get(self.LOGOUT_URL, **self.client_env(admin=False))
        self.assertEqual(resp.status_code, 404)
        resp = self.client.post(self.LOGOUT_URL, {}, **self.client_env(admin=False))
        self.assertEqual(resp.status_code, 404)

        self.login_staff1()
        resp = self.client.get(self.LOGOUT_URL, **self.client_env(admin=True))
        self.assertRedirects(resp,
                self.LOGIN_URL,
                status_code=302, target_status_code=200,
                fetch_redirect_response=True)

        self.login_staff1()
        resp = self.client.post(self.LOGOUT_URL, {}, **self.client_env(admin=True))
        self.assertRedirects(resp,
                self.LOGIN_URL,
                status_code=302, target_status_code=200,
                fetch_redirect_response=True)

        self.login_staff1()
        resp = self.client.get(self.ADMIN_LOGOUT_URL, **self.client_env(admin=True))
        self.assertRedirects(resp,
                self.ADMIN_URL,
                status_code=302, target_status_code=302,
                fetch_redirect_response=True)

        self.login_staff1()
        resp = self.client.post(self.ADMIN_LOGOUT_URL, {},
                **self.client_env(admin=True))
        self.assertRedirects(resp,
                self.ADMIN_URL,
                status_code=302, target_status_code=302,
                fetch_redirect_response=True)


    def test_admin(self):
        """When admin accesses the page
        """
        User = get_user_model()
        _logger.info(', '.join(x.username for x in User.objects.all()))

        self.login_admin1()
        resp = self.client.get(self.LOGOUT_URL, **self.client_env(admin=False))
        self.assertEqual(resp.status_code, 404)
        resp = self.client.post(self.LOGOUT_URL, {}, **self.client_env(admin=False))
        self.assertEqual(resp.status_code, 404)

        self.login_admin1()
        resp = self.client.get(self.LOGOUT_URL, **self.client_env(admin=True))
        self.assertRedirects(resp,
                self.LOGIN_URL,
                status_code=302, target_status_code=200,
                fetch_redirect_response=True)

        self.login_admin1()
        resp = self.client.post(self.LOGOUT_URL, {}, **self.client_env(admin=True))
        self.assertRedirects(resp,
                self.LOGIN_URL,
                status_code=302, target_status_code=200,
                fetch_redirect_response=True)

        self.login_admin1()
        resp = self.client.get(self.ADMIN_LOGOUT_URL, **self.client_env(admin=True))
        self.assertEqual(resp.status_code, 405)

        self.login_admin1()
        resp = self.client.post(self.ADMIN_LOGOUT_URL, {},
                **self.client_env(admin=True))
        self.assertRedirects(resp,
                '/',
                status_code=302, target_status_code=302,
                fetch_redirect_response=True)
