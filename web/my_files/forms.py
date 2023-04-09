"""Django forms for working with files
"""
from django.forms import ModelForm
#-
from .models import MyFile

class MyFileForm(ModelForm):
    """Form definition for file model
    """
    class Meta:
        model = MyFile
        fields = ('databits',
                *MyFile.description.fields,
                *MyFile.alt_text.fields)
