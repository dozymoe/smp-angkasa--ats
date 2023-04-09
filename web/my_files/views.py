"""Django views for working with files
"""
import logging
import os
#-
from django.conf import settings
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
#-
from my_files.models import MyFile

_logger = logging.getLogger(__name__)


def serve_files(request, pk, style=None):
    """Serve stored files
    """
    obj = get_object_or_404(MyFile, pk=pk)
    filename = obj.databits.name
    if obj.is_image() and style:
        for imgsize in settings.IMAGE_SIZES:
            if style == imgsize[0]:
                break
        else:
            raise Http404
        field = getattr(obj, f'image_{style}')
        if field:
            filename = field.name
    path = os.path.join(settings.MEDIA_ROOT, filename)
    return FileResponse(open(path, 'rb'))
