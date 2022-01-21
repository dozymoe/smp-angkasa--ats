import logging
#-
from django.contrib.auth.decorators import login_required
from django.urls import reverse
#from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView
#from django.views.generic import CreateView, DeleteView, DetailView, ListView
from django.views.generic import ListView
#from django.views.generic import UpdateView
from rules.contrib.views import AutoPermissionRequiredMixin
#-
from .models import MyFile

_logger = logging.getLogger(__name__)


@method_decorator(login_required, name='dispatch')
class List(ListView):
    model = MyFile
    paginate_by = 15


@method_decorator(login_required, name='dispatch')
class Create(CreateView):
    model = MyFile
    fields = ('databits', 'description', 'alt_text')
    template_name_suffix = '_create_form'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


    def get_success_url(self):
        return reverse('MyFile:Index')


@method_decorator(login_required, name='dispatch')
class Destroy(AutoPermissionRequiredMixin, DeleteView):
    model = MyFile

    def get_success_url(self):
        return reverse('MyFile:Index')