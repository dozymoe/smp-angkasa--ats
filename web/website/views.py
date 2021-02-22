from django.views.generic import TemplateView


class Home(TemplateView):
    template_name = 'website/welcome.html'


class VisiMisi(TemplateView):
    template_name = 'website/visi-misi.html'


class Ppdb(TemplateView):
    template_name = 'website/ppdb.html'
