"""Django forms for working with slideshows
"""
from django.forms import ModelForm
#-
from .models import MySlide

class MySlideForm(ModelForm):
    """Form definition for slide model
    """
    class Meta:
        model = MySlide
        fields = ['location', 'image',
                *MySlide.description.fields]
