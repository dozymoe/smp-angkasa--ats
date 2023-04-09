"""Test the management pages for files
"""
import logging
#-
from django.contrib.auth import get_user_model
from yarl import URL
#-
from my_files.models import MyFile
from web.testcases.testcase import SmpTestCase

_logger = logging.getLogger(__name__)

class TestManageFileDeletePage(SmpTestCase):
    """Test administration page for deleting files
    """
    user = None
    fileobj = None

    @classmethod
    def setUpTestData(cls):
        """Prepare testing data
        """
        cls.user = get_user_model().objects.get(username=cls.USER1_USERNAME)


    def setUp(self):
        """Prepare testing data
        """
        self.fileobj = MyFile.objects.create(
                databits=self.random_image(),
                description_id="Periksa ubah berkas",
                description_en="Test update file",
                created_by=self.user)


    def tearDown(self):
        """Cleanup
        """
        # file has been updated, not the same
        try:
            self.fileobj.delete()
        except MyFile.DoesNotExist:
            pass


    ## GET

    def test_anon_get(self):
        """When anon user access file delete page
        """
        base_url = URL('/files')
        url = base_url / str(self.fileobj.id) / 'delete'

        resp = self.client.get(url, **self.client_env(admin=True))
        self.assertRedirects(resp,
                URL('/account/login/') % {'next': str(url)}, 302,
                target_status_code=200, fetch_redirect_response=True)


    def test_owner_get(self):
        """When file owner access file delete page
        """
        base_url = URL('/files')
        url = base_url / str(self.fileobj.id) / 'delete'

        self.login_user01()

        resp = self.client.get(url, **self.client_env(admin=True))
        self.assertEqual(resp.status_code, 200)


    def test_not_owner_get(self):
        """When not file owner access file delete page
        """
        base_url = URL('/files')
        url = base_url / str(self.fileobj.id) / 'delete'

        self.login_user02()

        resp = self.client.get(url, **self.client_env(admin=True))
        self.assertEqual(resp.status_code, 403)


    def test_staff_get(self):
        """When staff access file delete page
        """
        base_url = URL('/files')
        url = base_url / str(self.fileobj.id) / 'delete'

        self.login_staff01()

        resp = self.client.get(url, **self.client_env(admin=True))
        self.assertEqual(resp.status_code, 200)


    ## POST

    def test_anon_post(self):
        """When anon user delete a file
        """
        base_url = URL('/files')
        url = base_url / str(self.fileobj.id) / 'delete'

        resp = self.client.post(url, **self.client_env(admin=True))
        self.assertRedirects(resp,
                URL('/account/login/') % {'next': str(url)}, 302,
                target_status_code=200, fetch_redirect_response=True)


    def test_owner_post(self):
        """When file owner delete a file
        """
        base_url = URL('/files')
        url = base_url / str(self.fileobj.id) / 'delete'

        self.login_user01()

        resp = self.client.post(url, **self.client_env(admin=True))
        self.assertRedirects(resp,
                base_url / '', 302,
                target_status_code=200, fetch_redirect_response=True)


    def test_not_owner_post(self):
        """When not file owner delete a file
        """
        base_url = URL('/files')
        url = base_url / str(self.fileobj.id) / 'delete'

        self.login_user02()

        resp = self.client.post(url, **self.client_env(admin=True))
        self.assertEqual(resp.status_code, 403)


    def test_staff_post(self):
        """When staff delete a file
        """
        base_url = URL('/files')
        url = base_url / str(self.fileobj.id) / 'delete'

        self.login_staff01()

        resp = self.client.post(url, **self.client_env(admin=True))
        self.assertRedirects(resp,
                base_url / '', 302,
                target_status_code=200, fetch_redirect_response=True)
