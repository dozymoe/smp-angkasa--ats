"""Django middleware that conditionally serve different routes
"""
import logging
#-
from django.conf import settings

_logger = logging.getLogger(__name__)


class DomainUrlsMiddleware:
    """Serve admin routes if it was admin website domain name
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.is_admin = request.get_host() == settings.ALLOWED_HOSTS[0]
        if request.is_admin:
            request.urlconf = settings.ROOT_URLCONF + '_admin'
        else:
            request.urlconf = settings.ROOT_URLCONF

        response = self.get_response(request)
        return response
