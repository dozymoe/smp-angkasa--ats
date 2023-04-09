"""Django views for working with blog postings
"""
from django.views.generic import DetailView
from translated_fields import to_attribute
#-
from .models import BlogPosting

class Display(DetailView):
    """Show blog post to visitors
    """
    model = BlogPosting

    def get_slug_field(self):
        return to_attribute(self.slug_field, self.request.LANGUAGE_CODE)
