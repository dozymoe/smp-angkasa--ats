"""Django forms for working with web pages
"""
from django.conf import settings
from django.forms import ModelForm
from django.utils.text import slugify
from translated_fields import to_attribute
#-
from .models import WebPage

class WebPageForm(ModelForm):
    """Form definition for web page model
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Autofill slug
        if self.data:
            data = self.data.copy()

            for langcode, _ in settings.LANGUAGES:
                title_field = to_attribute('title', langcode)
                slug_field = to_attribute('slug', langcode)
                if data.get(title_field) and not data.get(slug_field):
                    # Skip if instance already has slug value
                    if not self.instance or\
                            not getattr(self.instance, slug_field, None):
                        data[slug_field] = slugify(data[title_field])
                        self.data = data


    class Meta:
        model = WebPage
        fields = [*WebPage.title.fields,
                *WebPage.body.fields,
                *WebPage.summary.fields,
                *WebPage.slug.fields]
