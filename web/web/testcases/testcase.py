"""Prepare test client

Test users are created in my_user/testing.py
Test sites are created in website/testing.py
"""
from io import BytesIO
import logging
import re
#-
from bs4 import BeautifulSoup
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.test import TestCase
from PIL import Image
from yarl import URL

_logger = logging.getLogger(__name__)

class SmpTestCase(TestCase):
    """Prepare model instances and configuration
    """
    ADMIN_URL = URL('/admin/')
    ADMIN_LOGIN_URL = URL('/admin/login/')
    LOGIN_URL = URL('/account/login/')

    USER1_USERNAME = 'user1'
    USER1_PASSWORD = 'user1pass'
    USER2_USERNAME = 'user2'
    USER2_PASSWORD = 'user2pass'

    STAFF1_USERNAME = 'staff1'
    STAFF1_PASSWORD = 'staff1pass'

    ADMIN1_USERNAME = 'admin1'
    ADMIN1_PASSWORD = 'admin1pass'

    BANNED1_USERNAME = 'banuser1'
    BANNED1_PASSWORD = 'banuser1pass'

    def login_user1(self):
        """Prepare login session
        """
        resp = self.client.login(username=self.USER1_USERNAME,
                password=self.USER1_PASSWORD)
        self.assertTrue(resp)
        return get_user_model().objects.filter(username=self.USER1_USERNAME).first()


    def login_user2(self):
        """Prepare login session
        """
        resp = self.client.login(username=self.USER2_USERNAME,
                password=self.USER2_PASSWORD)
        self.assertTrue(resp)
        return get_user_model().objects.filter(username=self.USER2_USERNAME).first()


    def login_staff1(self):
        """Prepare login session
        """
        resp = self.client.login(username=self.STAFF1_USERNAME,
                password=self.STAFF1_PASSWORD)
        self.assertTrue(resp)
        return get_user_model().objects.filter(username=self.STAFF1_USERNAME)\
                .first()


    def login_admin1(self):
        """Prepare login session
        """
        resp = self.client.login(username=self.ADMIN1_USERNAME,
                password=self.ADMIN1_PASSWORD)
        self.assertTrue(resp)
        return get_user_model().objects.filter(username=self.ADMIN1_USERNAME)\
                .first()


    def login_banned1(self):
        """Prepare login session
        """
        resp = self.client.login(username=self.BANNED1_USERNAME,
                password=self.BANNED1_PASSWORD)
        self.assertTrue(resp)
        return get_user_model().objects.filter(username=self.BANNED1_USERNAME)\
                .first()


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


    def assertNoFormErrors(self, response):
        """If status_code 200, check that there is no form error in the html

        Display the form error if exists
        """
        if response.status_code != 200:
            return

        textarr = []

        soup = BeautifulSoup(response.content, 'html.parser')
        input_err_els = soup.find_all('input', attrs={'aria-invalid': 'true'})
        for input_err_el in input_err_els:
            textarr.append(f"* {input_err_el['name']}")

            # Admin theme
            group_el = input_err_el.find_parent('div',
                    class_=re.compile(r'\bform-row\b'))
            if group_el:
                msg_group_els = group_el.find_all('ul', class_='errorlist')
                for msg_group_el in msg_group_els:
                    msg_els = msg_group_el.find_all('li')
                    for msg_el in msg_els:
                        textarr.append(f"  * {msg_el.getText().strip()}")
            # Carbon Design theme
            group_el = input_err_el.find_parent('div',
                    class_=re.compile(r'\bbx--form-item\b'))
            if group_el:
                msg_els = group_el.find_all('div', class_='bx--form-requirement')
                for msg_el in msg_els:
                    textarr.append(f"  * {msg_el.getText().strip()}")

        if textarr:
            self.fail('\nFound form errors:\n' + '\n'.join(textarr))
