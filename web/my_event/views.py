"""Django views for working with event
"""
from django.views.generic import DetailView
from translated_fields import to_attribute
#-
from website.decorators import thawed_class_view
#-
from .models import Event

@thawed_class_view()
class Display(DetailView):
    """Show event to visitors
    """
    model = Event

    def get_slug_field(self):
        return to_attribute(self.slug_field, self.request.LANGUAGE_CODE)
