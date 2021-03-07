import logging
#-
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, DetailView, ListView
from django.views.generic import UpdateView
from rules.contrib.views import AutoPermissionRequiredMixin
#-
from .models import BlogPosting

_logger = logging.getLogger(__name__)


@method_decorator(login_required, name='dispatch')
class List(ListView):
    model = BlogPosting
    paginate_by = 15


@method_decorator(login_required, name='dispatch')
class Create(CreateView):
    model = BlogPosting
    fields = ['title', 'body', 'summary', 'slug']
    template_name_suffix = '_create_form'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


    def get_success_url(self):
        return reverse('BlogPosting:Index')


@method_decorator(login_required, name='dispatch')
class Display(DetailView):
    model = BlogPosting
    template_name_suffix = '_detail-admin'


@method_decorator(login_required, name='dispatch')
class Edit(AutoPermissionRequiredMixin, UpdateView):
    model = BlogPosting
    fields = ['title', 'body', 'summary', 'slug']

    def get_success_url(self):
        return reverse('BlogPosting:Index')


@method_decorator(login_required, name='dispatch')
class Publish(AutoPermissionRequiredMixin, UpdateView):
    model = BlogPosting
    fields = []
    template_name_suffix = '_confirm_publish'

    def form_valid(self, form):
        form.instance.published_at = timezone.now()
        return super().form_valid(form)


    def get_success_url(self):
        return reverse('BlogPosting:Index')


@method_decorator(login_required, name='dispatch')
class Unpublish(AutoPermissionRequiredMixin, UpdateView):
    model = BlogPosting
    fields = []
    template_name_suffix = '_confirm_unpublish'

    def form_valid(self, form):
        form.instance.published_at = None
        return super().form_valid(form)


    def get_success_url(self):
        return reverse('BlogPosting:Index')


@method_decorator(login_required, name='dispatch')
class Destroy(AutoPermissionRequiredMixin, DeleteView):
    model = BlogPosting

    def get_success_url(self):
        return reverse('BlogPosting:Index')
