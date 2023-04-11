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
    def test_anon_get(self):
        """When anon user access file create form
        """
        base_url = URL('/files')

        resp = self.client.get(base_url / 'add',
                **self.client_env(admin=True))
        self.assertRedirects(resp,
                URL('/account/login/') % {'next': '/files/add'}, 302,
                target_status_code=200, fetch_redirect_response=True)


    def test_user_get(self):
        """When authenticated user access file create form
        """
        base_url = URL('/files')

        self.login_user01()

        resp = self.client.get(base_url / 'add',
                **self.client_env(admin=True))
        self.assertEqual(resp.status_code, 200)


    def test_anon_post(self):
        """When anon user create new file
        """
        base_url = URL('/files')
        tmp_file = self.random_image()

        resp = self.client.post(base_url / 'add',
                {
                    'databits': tmp_file,
                    'alt_text_id': "Berkas acak",
                    'alt_text_en': "Random file",
                },
                format='multipart',
                **self.client_env(admin=True))
        self.assertRedirects(resp,
                URL('/account/login/') % {'next': '/files/add'}, 302,
                target_status_code=200, fetch_redirect_response=True)


    def test_user_post(self):
        """When authenticated user create new file
        """
        base_url = URL('/files')
        tmp_file = self.random_image()

        self.login_user01()

        resp = self.client.post(base_url / 'add',
                {
                    'databits': tmp_file,
                    'alt_text_id': "Berkas acak",
                    'alt_text_en': "Random file",
                },
                format='multipart',
                **self.client_env(admin=True))

        self.assertEqual(resp.status_code, 302)
        object_id = int(resp['Location'].split('/')[-2])

        try:
            self.assertRedirects(resp,
                    base_url / f'{object_id}/edit', 302,
                    target_status_code=200, fetch_redirect_response=True)
        finally:
            MyFile.objects.get(id=object_id).delete()
