import logging
#-
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

_logger = logging.getLogger(__name__)


@method_decorator(login_required, name='dispatch')
class Home(TemplateView):
    template_name = 'website/welcome-admin.html'
