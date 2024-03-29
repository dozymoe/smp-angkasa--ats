"""Django views for managing web pages that will have its summary in front page
"""
import logging
#-
from django.contrib.auth.decorators import login_required
from django.db.models import F, Max
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, ListView
from rules.contrib.views import AutoPermissionRequiredMixin
#-
from .models import FrontContent

_logger = logging.getLogger(__name__)


@method_decorator(login_required, name='dispatch')
class List(ListView):
    """List all front contents
    """
    model = FrontContent
    paginate_by = 10
    ordering = ('position', '-created_at')

    def get_paginate_by(self, queryset):
        return self.request.GET.get('pagesize', self.paginate_by)


@method_decorator(login_required, name='dispatch')
class Create(CreateView):
    """Create new front content
    """
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
    """Delete front content
    """
    model = FrontContent

    def get_success_url(self):
        return reverse('FrontContent:Index')


@login_required
def move_first(request, pk):
    """Change the ordering position of front content
    """
    obj = get_object_or_404(FrontContent, pk=pk)
    # Position 0 is special, it's default value.
    if obj.position == 0:
        FrontContent.objects\
                .filter(position__gt=0)\
                .update(position=F('position') + 1)
        obj.position = 1
        obj.save()
    elif obj.position > 1:
        FrontContent.objects\
                .filter(position__gt=0, position__lt=obj.position)\
                .update(position=F('position') + 1)
        obj.position = 1
        obj.save()
    return redirect(request.GET['next'])


@login_required
def move_up(request, pk):
    """Change the ordering position of front content
    """
    obj = get_object_or_404(FrontContent, pk=pk)
    # Position 0 is special, it's default value.
    if obj.position == 0:
        FrontContent.objects\
                .filter(position__gt=0)\
                .update(position=F('position') + 1)
        obj.position = 1
        obj.save()
    elif obj.position > 1:
        FrontContent.objects\
                .filter(position=obj.position - 1)\
                .update(position=F('position') + 1)
        obj.position -= 1
        obj.save()
    return redirect(request.GET['next'])


@login_required
def move_down(request, pk):
    """Change the ordering position of front content
    """
    obj = get_object_or_404(FrontContent, pk=pk)
    # Position 0 is special, it's default value.
    if obj.position == 0:
        FrontContent.objects\
                .filter(position__gt=0)\
                .update(position=F('position') + 1)
        obj.position = 1
        obj.save()
    else:
        FrontContent.objects\
                .filter(position=obj.position + 1)\
                .update(position=F('position') - 1)
        obj.position += 1
        obj.save()
    return redirect(request.GET['next'])


@login_required
def move_last(request, pk):
    """Change the ordering position of front content
    """
    obj = get_object_or_404(FrontContent, pk=pk)
    max_value = FrontContent.objects\
            .aggregate(Max('position'))\
            .get('position__max')
    # Position 0 is special, it's default value.
    if obj.position == 0:
        obj.position = max_value + 1
        obj.save()
    elif obj.position != max_value:
        FrontContent.objects\
                .filter(position__gt=obj.position)\
                .update(position=F('position') - 1)
        obj.position = max_value
        obj.save()
    return redirect(request.GET['next'])
