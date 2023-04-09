"""Django views for managing blog postings
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
from .forms import BlogPostingForm
from .models import BlogPosting

_logger = logging.getLogger(__name__)


@method_decorator(login_required, name='dispatch')
class List(ListView):
    """List all blog posts
    """
    model = BlogPosting
    paginate_by = 10

    def get_paginate_by(self, queryset):
        return self.request.GET.get('pagesize', self.paginate_by)


@method_decorator(login_required, name='dispatch')
class Create(CreateView):
    """Create new blog post
    """
    model = BlogPosting
    form_class = BlogPostingForm
    template_name_suffix = '_create_form'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


    def get_success_url(self):
        return reverse('BlogPosting:Index')


@method_decorator(login_required, name='dispatch')
class Display(DetailView):
    """Show blog post to visitors
    """
    model = BlogPosting
    template_name_suffix = '_detail-admin'


@method_decorator(login_required, name='dispatch')
class Edit(AutoPermissionRequiredMixin, UpdateView):
    """Edit blog post
    """
    model = BlogPosting
    form_class = BlogPostingForm

    def get_success_url(self):
        return reverse('BlogPosting:Index')


@method_decorator(login_required, name='dispatch')
class Publish(AutoPermissionRequiredMixin, UpdateView):
    """Publish a blog post
    """
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
    """Cancel published blog post
    """
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
    """Delete blog post
    """
    model = BlogPosting

    def get_success_url(self):
        return reverse('BlogPosting:Index')
