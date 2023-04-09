"""Django views for managing web pages
"""
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
from .forms import WebPageForm
from .models import WebPage

_logger = logging.getLogger(__name__)


@method_decorator(login_required, name='dispatch')
class List(ListView):
    """List all web pages
    """
    model = WebPage
    paginate_by = 10

    def get_paginate_by(self, queryset):
        return self.request.GET.get('pagesize', self.paginate_by)


@method_decorator(login_required, name='dispatch')
class Create(CreateView):
    """Create new web page
    """
    model = WebPage
    form_class = WebPageForm
    template_name_suffix = '_create_form'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


    def get_success_url(self):
        return reverse('WebPage:Index')


@method_decorator(login_required, name='dispatch')
class Display(DetailView):
    """Show web page to visitors
    """
    model = WebPage
    template_name_suffix = '_detail-admin'


@method_decorator(login_required, name='dispatch')
class Edit(AutoPermissionRequiredMixin, UpdateView):
    """Edit web page
    """
    model = WebPage
    form_class = WebPageForm

    def get_success_url(self):
        return reverse('WebPage:Index')


@method_decorator(login_required, name='dispatch')
class Publish(AutoPermissionRequiredMixin, UpdateView):
    """Publish web page
    """
    model = WebPage
    fields = []
    template_name_suffix = '_confirm_publish'

    def form_valid(self, form):
        form.instance.published_at = timezone.now()
        return super().form_valid(form)


    def get_success_url(self):
        return reverse('WebPage:Index')


@method_decorator(login_required, name='dispatch')
class Unpublish(AutoPermissionRequiredMixin, UpdateView):
    """Cancel a published web page
    """
    model = WebPage
    fields = []
    template_name_suffix = '_confirm_unpublish'

    def form_valid(self, form):
        form.instance.published_at = None
        return super().form_valid(form)


    def get_success_url(self):
        return reverse('WebPage:Index')


@method_decorator(login_required, name='dispatch')
class Destroy(AutoPermissionRequiredMixin, DeleteView):
    """Delete web page
    """
    model = WebPage

    def get_success_url(self):
        return reverse('WebPage:Index')
