from django.forms import ModelForm
#-
from .models import Event

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['started_at', 'stopped_at',
                *Event.title.fields,
                *Event.slug.fields,
                *Event.body.fields,
                *Event.summary.fields]
