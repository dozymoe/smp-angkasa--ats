from django.utils import timezone
from django.views.generic import TemplateView
#-
from blog_posting.models import BlogPosting
from my_event.models import Event
from my_front_content.models import FrontContent
from my_slide.models import MySlide


class Home(TemplateView):
    template_name = 'website/welcome.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()

        context['blogposts'] = BlogPosting.objects\
                .filter(published_at__isnull=False)\
                .all()[:10]
        context['events'] = Event.objects\
                .filter(
                    published_at__isnull=False,
                    started_at__gte=now)\
                .order_by('started_at')\
                .all()[:10]
        context['slides'] = MySlide.objects\
                .filter(location='front')\
                .all()[:20]
        context['front_contents'] = FrontContent.objects.all()[:3]
        return context


class EditorHelpText(TemplateView):
    template_name = 'website/editor-helptext.html'
