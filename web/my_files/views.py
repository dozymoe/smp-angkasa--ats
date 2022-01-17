import logging
import os
#-
from django.conf import settings
from django.http import HttpResponse
from django.utils.encoding import smart_str

_logger = logging.getLogger(__name__)


def serve_files(request, path):
    response = HttpResponse()
    response['X-Sendfile'] = smart_str(os.path.join(settings.MEDIA_ROOT, path))
    return response
