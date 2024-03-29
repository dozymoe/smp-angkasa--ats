"""Django views for miscellaneous admin pages
"""
import logging
#-
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, View
#-
from website.templatetags.website import restructured_text

_logger = logging.getLogger(__name__)


@method_decorator(login_required, name='dispatch')
class Home(TemplateView):
    """Admin welcome page
    """
    template_name = 'website/welcome-admin.html'


@method_decorator(login_required, name='dispatch')
class ReSTPreview(View):
    """Format request body using docutils reStructuredText
    """
    def post(self, request):
        """Render reStructuredText into html
        """
        parsed = restructured_text(request.POST['body'])
        return HttpResponse(parsed, content_type='text/plain')
