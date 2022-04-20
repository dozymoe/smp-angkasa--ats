from django.forms import ModelForm
#-
from .models import MySlide

class MySlideForm(ModelForm):
    class Meta:
        model = MySlide
        fields = ['location', 'image',
                *MySlide.description.fields]
