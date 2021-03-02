import logging
#-
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, View
from docutils.core import publish_parts

_logger = logging.getLogger(__name__)


@method_decorator(login_required, name='dispatch')
class Home(TemplateView):
    template_name = 'website/welcome-admin.html'


@method_decorator(login_required, name='dispatch')
class ReSTPreview(View):

    def post(self, request):
        parts = publish_parts(request.POST['body'], writer_name='html',
                settings_overrides=settings.RESTRUCTURED_TEXT)
        return HttpResponse(parts['html_body'], content_type='text/plain')
