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

class TestManageFileUpdatePage(SmpTestCase):
    """Test administration page for updating files
    """
    BASE_URL = URL('/files/')

    fileobj = None

    def setUp(self):
        """Prepare testing data
        """
        user = get_user_model().objects.filter(username=self.USER1_USERNAME).first()
        self.fileobj = MyFile.objects.create(
                databits=self.random_image(),
                alt_text_id="Periksa ubah berkas",
                alt_text_en="Test update file",
                created_by=user)


    def tearDown(self):
        """Cleanup
        """
        # file has been updated, not the same
        self.fileobj.refresh_from_db()
        self.fileobj.delete()


    def test_anon_get(self):
        """When anon user access file edit form
        """
        url = self.BASE_URL / str(self.fileobj.id) / 'edit'

        resp = self.client.get(url, **self.client_env(admin=True))
        self.assertRedirects(resp,
                self.LOGIN_URL % {'next': str(url)},
                302, target_status_code=200, fetch_redirect_response=True)


    def test_user_get(self):
        """When authenticated user access file edit form
        """
        url = self.BASE_URL / str(self.fileobj.id) / 'edit'

        self.login_user1()

        resp = self.client.get(url, **self.client_env(admin=True))
        self.assertEqual(resp.status_code, 200)


    def test_anon_post(self):
        """When anon user update a file
        """
        url = self.BASE_URL / str(self.fileobj.id) / 'edit'
        tmp_file = self.random_image()

        resp = self.client.post(url,
                {
                    'databits': tmp_file,
                    'alt_text_id': "Berkas acak",
                    'alt_text_en': "Random file",
                },
                format='multipart',
                **self.client_env(admin=True))
        self.assertNoFormErrors(resp)
        self.assertRedirects(resp,
                self.LOGIN_URL % {'next': str(url)},
                302, target_status_code=200, fetch_redirect_response=True)


    def test_user_post(self):
        """When authenticated user update a file
        """
        url = self.BASE_URL / str(self.fileobj.id) / 'edit'
        tmp_file = self.random_image()

        self.login_user1()

        resp = self.client.post(url,
                {
                    'databits': tmp_file,
                    'alt_text_id': "Berkas acak",
                    'alt_text_en': "Random file",
                },
                format='multipart',
                **self.client_env(admin=True))
        self.assertNoFormErrors(resp)
        self.assertRedirects(resp,
                self.BASE_URL,
                302, target_status_code=200, fetch_redirect_response=True)
