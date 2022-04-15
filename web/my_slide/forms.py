from django.forms import ModelForm
#-
from .models import MySlide

class MySlideForm(ModelForm):
    class Meta:
        model = MySlide
        exclude = []
        #fields = ['location', 'image', 'description']
