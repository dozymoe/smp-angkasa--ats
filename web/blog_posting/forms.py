"""Django forms for working with blog postings
"""
from django import forms
from django.conf import settings
from django.utils.text import slugify
from translated_fields import to_attribute
#-
from .models import BlogPosting

class BlogPostingForm(forms.ModelForm):
    """Form definition for blog post model
    """
    image_label = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.image:
            self.initial.setdefault('image_label',
                    self.instance.image.description)

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
        model = BlogPosting
        fields = ['image', 'image_label',
                *BlogPosting.title.fields,
                *BlogPosting.slug.fields,
                *BlogPosting.body.fields,
                *BlogPosting.summary.fields]
