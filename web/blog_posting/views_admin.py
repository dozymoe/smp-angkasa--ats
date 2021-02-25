import logging
#-
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView
#-
from .models import BlogPosting

_logger = logging.getLogger(__name__)


@method_decorator(login_required, name='dispatch')
class Create(CreateView):
    model = BlogPosting
    fields = ['title', 'body', 'summary', 'slug']
    template_name_suffix = '_create_form'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


    def get_success_url(self):
        return reverse('BlogPosting:Edit', (self.object.pk,))
