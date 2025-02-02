"""Tell allauth to disable user registration
"""
import logging
#-
from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings

_logger = logging.getLogger(__name__)

class NoNewUsersAccountAdapter(DefaultAccountAdapter):
    """Account Adapter that disables user registration
    """
    def is_open_for_signup(self, request):
        """
        Checks whether or not the site is open for signups.

        Next to simply returning True/False you can also intervene the
        regular flow by raising an ImmediateHttpResponse

        (Comment reproduced from the overridden method.)
        """
        return False


    def authenticate(self, request, **credentials):
        """Allow authentication based on hostnames
        """
        # We only have logins for the admin sites
        if request.site and request.site.domain == settings.ALLOWED_HOSTS[0]:
            user = super().authenticate(request, **credentials)
            # Is admin site
            #route_name = request.resolver_match.url_name
            #if route_name == 'account_login':
            if user and not (user.is_staff or user.is_superuser):
                return None
        else:
            user = None
        return user
