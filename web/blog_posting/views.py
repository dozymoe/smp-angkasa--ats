import logging
#-
from django.views.generic import DetailView
#-
from .models import BlogPosting

_logger = logging.getLogger(__name__)


class Display(DetailView):
    model = BlogPosting
