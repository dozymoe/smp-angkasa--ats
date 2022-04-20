from django.forms import ModelForm
#-
from .models import MyFile

class MyFileForm(ModelForm):
    class Meta:
        model = MyFile
        fields = ('databits',
                *MyFile.description.fields,
                *MyFile.alt_text.fields)
