"""Django views for miscellaneous pages
"""
from django.urls import reverse
from django.shortcuts import redirect
from django.utils import timezone
from django.views.generic import TemplateView
#-
from blog_posting.models import BlogPosting
from my_event.models import Event
from my_front_content.models import FrontContent
from my_slide.models import MySlide

class Home(TemplateView):
    """Show home page to visitors
    """
    template_name = 'website/welcome.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()

        context['blogposts'] = BlogPosting.objects\
                .filter(
                    published_at__isnull=False,
                    deleted_at__isnull=True)\
                .order_by('-published_at')\
                .all()[:4]
        context['events'] = Event.objects\
                .filter(
                    published_at__isnull=False,
                    deleted_at__isnull=True,
                    started_at__gte=now)\
                .order_by('started_at')\
                .all()[:10]
        context['slides'] = MySlide.objects\
                .filter(location='front')\
                .order_by('position', '-created_at')\
                .all()[:20]
        context['front_contents'] = FrontContent.objects\
                .order_by('position', '-created_at')\
                .all()[:3]
        return context


class EditorHelpText(TemplateView):
    """Show the editor help text
    """
    template_name = 'website/editor-helptext.html'


def home(request):
    """Redirect from non multilingual home page
    """
    return redirect(reverse('HomeLang', args=('html',)))
