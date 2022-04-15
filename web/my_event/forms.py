from django.forms import ModelForm
#-
from .models import Event

class EventForm(ModelForm):
    class Meta:
        model = Event
        exclude = []
        #fields = ['title', 'body', 'summary', 'slug', 'started_at',
        #        'stopped_at']
