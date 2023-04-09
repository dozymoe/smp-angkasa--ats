"""Prepare test client

Test users are created in my_user/testing.py
Test sites are created in website/testing.py
"""
from io import BytesIO
import logging
#-
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.test import TestCase
from PIL import Image
from yarl import URL

_logger = logging.getLogger(__name__)


class SmpTestCase(TestCase):
    """Prepare model instances and configuration
    """
    LOGIN_URL = URL('/account/login/')

    USER1_USERNAME = 'user1'
    USER1_PASSWORD = 'user1pass'
    USER2_USERNAME = 'user2'
    USER2_PASSWORD = 'user2pass'

    STAFF1_USERNAME = 'staff1'
    STAFF1_PASSWORD = 'staff1pass'


    def login_user01(self):
        """Prepare login session
        """
        resp = self.client.login(username=self.USER1_USERNAME,
                password=self.USER1_PASSWORD)
        self.assertTrue(resp)


    def login_user02(self):
        """Prepare login session
        """
        resp = self.client.login(username=self.USER2_USERNAME,
                password=self.USER2_PASSWORD)
        self.assertTrue(resp)


    def login_staff01(self):
        """Prepare login session
        """
        resp = self.client.login(username=self.STAFF1_USERNAME,
                password=self.STAFF1_PASSWORD)
        self.assertTrue(resp)


    def client_env(self, admin=False):
        """Set Django request META data
        """
        # This is needed for multisites (management and normal web)
        server_name = settings.ALLOWED_HOSTS[0 if admin else 1]
        return {'SERVER_NAME': server_name}


    @classmethod
    def random_image(cls, width=400, height=300):
        """Create in memory random image for testing file upload
        """
        tmp_img = Image.new(mode='RGB', size=(width, height), color='pink')
        tmp_buf = BytesIO()
        tmp_img.save(tmp_buf, format='jpeg')
        tmp_size = tmp_buf.tell()
        tmp_buf.seek(0)

        return InMemoryUploadedFile(tmp_buf, None, 'file.jpg', 'image/jpeg',
                tmp_size, None)
