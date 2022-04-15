from django.forms import ModelForm
#-
from .models import MyFile

class MyFileForm(ModelForm):
    class Meta:
        model = MyFile
        exclude = []
        #fields = ('databits', 'description', 'alt_text')
