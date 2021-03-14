from django.views.generic import TemplateView
#-
from blog_posting.models import BlogPosting


class Home(TemplateView):
    template_name = 'website/welcome.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blogposts'] = BlogPosting.objects\
                .filter(published_at__isnull=False)\
                .all()[:10]
        return context


class VisiMisi(TemplateView):
    template_name = 'website/visi-misi.html'


class Ppdb(TemplateView):
    template_name = 'website/ppdb.html'


class EditorHelpText(TemplateView):
    template_name = 'website/editor-helptext.html'
