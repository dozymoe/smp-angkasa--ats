"""Django views for working with blog postings
"""
from django.views.generic import DetailView
from translated_fields import to_attribute
#-
from website.decorators import thawed_class_view
#-
from .models import BlogPosting

@thawed_class_view()
class Display(DetailView):
    """Show blog post to visitors
    """
    model = BlogPosting

    def get_slug_field(self):
        return to_attribute(self.slug_field, self.request.LANGUAGE_CODE)
