from django.forms import ModelForm
#-
from .models import WebPage

class WebPageForm(ModelForm):
    class Meta:
        model = WebPage
        fields = [*WebPage.title.fields,
                *WebPage.body.fields,
                *WebPage.summary.fields,
                *WebPage.slug.fields]
