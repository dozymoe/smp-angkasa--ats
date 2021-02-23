import logging
#-
from django.conf import settings

_logger = logging.getLogger(__name__)


class DomainUrlsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.site.id == 2:
            request.urlconf = settings.ROOT_URLCONF + '_admin'
        else:
            request.urlconf = settings.ROOT_URLCONF

        response = self.get_response(request)
        return response
