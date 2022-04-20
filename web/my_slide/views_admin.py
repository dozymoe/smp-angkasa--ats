import logging
#-
from django.contrib.auth.decorators import login_required
from django.db.models import F, Max
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from rules.contrib.views import AutoPermissionRequiredMixin
#-
from .forms import MySlideForm
from .models import MySlide

_logger = logging.getLogger(__name__)


@method_decorator(login_required, name='dispatch')
class List(ListView):
    model = MySlide
    paginate_by = 10
    ordering = ('position', '-created_at')

    def get_paginate_by(self, queryset):
        return self.request.GET.get('pagesize', self.paginate_by)


@method_decorator(login_required, name='dispatch')
class Create(CreateView):
    model = MySlide
    form_class = MySlideForm
    template_name_suffix = '_create_form'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


    def get_success_url(self):
        return reverse('MySlide:Index')


@method_decorator(login_required, name='dispatch')
class Edit(AutoPermissionRequiredMixin, UpdateView):
    model = MySlide
    form_class = MySlideForm

    def get_success_url(self):
        return reverse('MySlide:Index')


@method_decorator(login_required, name='dispatch')
class Destroy(AutoPermissionRequiredMixin, DeleteView):
    model = MySlide

    def get_success_url(self):
        return reverse('MySlide:Index')


@login_required
def move_first(request, pk):
    obj = get_object_or_404(MySlide, pk=pk)
    # Position 0 is special, it's default value.
    if obj.position == 0:
        MySlide.objects\
                .filter(position__gt=0)\
                .update(position=F('position') + 1)
        obj.position = 1
        obj.save()
    elif obj.position > 1:
        MySlide.objects\
                .filter(position__gt=0, position__lt=obj.position)\
                .update(position=F('position') + 1)
        obj.position = 1
        obj.save()
    return redirect(request.GET['next'])

@login_required
def move_up(request, pk):
    obj = get_object_or_404(MySlide, pk=pk)
    # Position 0 is special, it's default value.
    if obj.position == 0:
        MySlide.objects\
                .filter(position__gt=0)\
                .update(position=F('position') + 1)
        obj.position = 1
        obj.save()
    elif obj.position > 1:
        MySlide.objects\
                .filter(position=obj.position - 1)\
                .update(position=F('position') + 1)
        obj.position -= 1
        obj.save()
    return redirect(request.GET['next'])

@login_required
def move_down(request, pk):
    obj = get_object_or_404(MySlide, pk=pk)
    # Position 0 is special, it's default value.
    if obj.position == 0:
        MySlide.objects\
                .filter(position__gt=0)\
                .update(position=F('position') + 1)
        obj.position = 1
        obj.save()
    else:
        MySlide.objects\
                .filter(position=obj.position + 1)\
                .update(position=F('position') - 1)
        obj.position += 1
        obj.save()
    return redirect(request.GET['next'])

@login_required
def move_last(request, pk):
    obj = get_object_or_404(MySlide, pk=pk)
    max_value = MySlide.objects\
            .aggregate(Max('position'))\
            .get('position__max')
    # Position 0 is special, it's default value.
    if obj.position == 0:
        obj.position = max_value + 1
        obj.save()
    elif obj.position != max_value:
        MySlide.objects\
                .filter(position__gt=obj.position)\
                .update(position=F('position') - 1)
        obj.position = max_value
        obj.save()
    return redirect(request.GET['next'])
