import logging
#-
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, ListView
from rules.contrib.views import AutoPermissionRequiredMixin
#-
from .models import FrontContent

_logger = logging.getLogger(__name__)


@method_decorator(login_required, name='dispatch')
class List(ListView):
    model = FrontContent
    paginate_by = 15


@method_decorator(login_required, name='dispatch')
class Create(CreateView):
    model = FrontContent
    fields = ['content']
    template_name_suffix = '_create_form'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


    def get_success_url(self):
        return reverse('FrontContent:Index')


@method_decorator(login_required, name='dispatch')
class Destroy(AutoPermissionRequiredMixin, DeleteView):
    model = FrontContent

    def get_success_url(self):
        return reverse('FrontContent:Index')
