import logging
import os
#-
from django.conf import settings
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from translated_fields import to_attribute
#-
from .models import BlogPosting

_logger = logging.getLogger(__name__)


class Display(DetailView):
    model = BlogPosting

    def get_slug_field(self):
        return to_attribute(self.slug_field, self.request.LANGUAGE_CODE)


def serve_files(request, pk, style=None):
    obj = get_object_or_404(BlogPosting, pk=pk)
    if style is None:
        field = obj.image
    else:
        for imgsize in settings.IMAGE_SIZES:
            if style == imgsize[0]:
                break
        else:
            raise Http404
        field = getattr(obj, f'image_{style}')
        if not field:
            field = obj.image
    if not field:
        raise Http404
    path = os.path.join(settings.MEDIA_ROOT, field.name)
    return FileResponse(open(path, 'rb'))
