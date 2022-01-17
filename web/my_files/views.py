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
    obj = get_object_or_404(MyFile, pk=pk)
    if obj.is_image():
        for imgsize in settings.IMAGE_SIZES:
            if style == imgsize[0]:
                break
        else:
            raise Http404
        field = getattr(obj, 'image_' + style)
        if not field:
            field = obj.databits
    else:
        field = obj.databits
    path = os.path.join(settings.MEDIA_ROOT, field.name)
    return FileResponse(open(path, 'rb'))
