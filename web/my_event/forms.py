"""Django forms for working with events
"""
from datetime import datetime
#-
from django import forms
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify
import pytz
from translated_fields import to_attribute
#-
from .models import Event

class EventForm(forms.ModelForm):
    """Form definition for event model
    """
    started_at = forms.DateTimeField(required=False) # disable model required
    started_date = forms.DateField()
    started_time = forms.TimeField()
    started_timezone = forms.ChoiceField(choices=[
            (tz, tz) for tz in pytz.common_timezones])

    stopped_date = forms.DateField(required=False)
    stopped_time = forms.TimeField(required=False)
    stopped_timezone = forms.ChoiceField(choices=[
            (tz, tz) for tz in pytz.common_timezones])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        current_tz = timezone.get_current_timezone()

        if self.instance and self.instance.started_at:
            dt = self.instance.started_at.astimezone(current_tz)
            self.initial.setdefault('started_date', dt.date())
            self.initial.setdefault('started_time', dt.time().strftime('%H:%M'))
            self.initial.setdefault('started_timezone', dt.tzinfo.key)
        else:
            self.initial.setdefault('started_timezone', settings.TIME_ZONE)

        if self.instance and self.instance.stopped_at:
            dt = self.instance.stopped_at.astimezone(current_tz)
            self.initial.setdefault('stopped_date', dt.date())
            self.initial.setdefault('stopped_time', dt.time().strftime('%H:%M'))
            self.initial.setdefault('stopped_timezone', dt.tzinfo.key)
        else:
            self.initial.setdefault('stopped_timezone', settings.TIME_ZONE)

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


    def clean(self):
        """Join the datetime that has been separated into date and time
        """
        dt = datetime.combine(self.cleaned_data['started_date'],
                self.cleaned_data['started_time'])
        dt = pytz.timezone(self.cleaned_data['started_timezone']).localize(dt)
        self.cleaned_data['started_at'] = dt

        if self.cleaned_data.get('stopped_date'):
            dt = datetime.combine(self.cleaned_data['stopped_date'],
                    self.cleaned_data['stopped_time'])
            dt = pytz.timezone(self.cleaned_data['stopped_timezone'])\
                    .localize(dt)
            self.cleaned_data['stopped_at'] = dt


    class Meta:
        model = Event
        fields = ['started_at', 'started_date', 'started_time',
                'stopped_at', 'stopped_date', 'stopped_time',
                *Event.title.fields,
                *Event.slug.fields,
                *Event.body.fields,
                *Event.summary.fields]
