"""Create shared users for integration tests
"""
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
#-
from web.testcases.testcase import SmpTestCase

def create_test_users(sender, **kwargs):
    """Create test users
    """
    # This is set in DiscoveryRunner
    if not settings.TESTING:
        return

    User = get_user_model()
    TestCase = SmpTestCase

    User.objects.create(username=TestCase.USER1_USERNAME,
            password=make_password(TestCase.USER1_PASSWORD),
            is_staff=False, is_active=True)
    User.objects.create(username=TestCase.USER2_USERNAME,
            password=make_password(TestCase.USER2_PASSWORD),
            is_staff=False, is_active=True)
    User.objects.create(username=TestCase.STAFF1_USERNAME,
            password=make_password(TestCase.STAFF1_PASSWORD),
            is_staff=True, is_active=True)
