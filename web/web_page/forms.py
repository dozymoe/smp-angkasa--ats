from django.forms import ModelForm
#-
from .models import WebPage

class WebPageForm(ModelForm):
    class Meta:
        model = WebPage
        exclude = []
        #fields = ['title', 'body', 'summary', 'slug']
