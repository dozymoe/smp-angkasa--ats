from django.views.generic import DetailView
#-
from .models import Event


class Display(DetailView):
    model = Event
