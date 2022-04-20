import logging
#-
from django.views.generic import DetailView
from translated_fields import to_attribute
#-
from .models import WebPage

_logger = logging.getLogger(__name__)


class Display(DetailView):
    model = WebPage

    def get_slug_field(self):
        return to_attribute(self.slug_field, self.request.LANGUAGE_CODE)
