"""Test the management pages for files
"""
import logging
#-
from yarl import URL
#-
from my_files.models import MyFile
from web.testcases.testcase import SmpTestCase

_logger = logging.getLogger(__name__)

class TestManageFileCreatePage(SmpTestCase):
    """Test administration page for creating files
    """
    BASE_URL = URL('/files/')
    CREATE_URL = BASE_URL / 'add'

    def test_anon_get(self):
        """When anon user access file create form
        """
        resp = self.client.get(self.CREATE_URL, **self.client_env(admin=False))
        self.assertEqual(resp.status_code, 404)

        resp = self.client.get(self.CREATE_URL, **self.client_env(admin=True))
        self.assertRedirects(resp,
                self.LOGIN_URL % {'next': str(self.CREATE_URL)},
                302, target_status_code=200, fetch_redirect_response=True)


    def test_user_get(self):
        """When authenticated user access file create form
        """
        self.login_user1()
        resp = self.client.get(self.CREATE_URL, **self.client_env(admin=False))
        self.assertEqual(resp.status_code, 404)

        resp = self.client.get(self.CREATE_URL, **self.client_env(admin=True))
        self.assertEqual(resp.status_code, 200)


    def test_anon_post(self):
        """When anon user create new file
        """
        tmp_file = self.random_image()

        resp = self.client.post(self.CREATE_URL,
                {
                    'databits': tmp_file,
                    'alt_text_id': "Berkas acak",
                    'alt_text_en': "Random file",
                },
                format='multipart',
                **self.client_env(admin=False))
        self.assertEqual(resp.status_code, 404)

        resp = self.client.post(self.CREATE_URL,
                {
                    'databits': tmp_file,
                    'alt_text_id': "Berkas acak",
                    'alt_text_en': "Random file",
                },
                format='multipart',
                **self.client_env(admin=True))
        self.assertNoFormErrors(resp)
        self.assertRedirects(resp,
                self.LOGIN_URL % {'next': str(self.CREATE_URL)},
                302, target_status_code=200, fetch_redirect_response=True)


    def test_user_post(self):
        """When authenticated user create new file
        """
        tmp_file = self.random_image()

        self.login_user1()

        resp = self.client.post(self.CREATE_URL,
                {
                    'databits': tmp_file,
                    'alt_text_id': "Berkas acak",
                    'alt_text_en': "Random file",
                },
                format='multipart',
                **self.client_env(admin=False))
        self.assertEqual(resp.status_code, 404)

        tmp_file.seek(0)
        resp = self.client.post(self.CREATE_URL,
                {
                    'databits': tmp_file,
                    'alt_text_id': "Berkas acak",
                    'alt_text_en': "Random file",
                },
                format='multipart',
                **self.client_env(admin=True))
        self.assertNoFormErrors(resp)
        self.assertEqual(resp.status_code, 302)
        object_id = int(resp['Location'].split('/')[-2])

        try:
            self.assertRedirects(resp,
                    self.BASE_URL / f'{object_id}/edit', 302,
                    target_status_code=200, fetch_redirect_response=True)
        finally:
            MyFile.objects.get(id=object_id).delete()
