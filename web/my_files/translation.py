from modeltranslation.translator import register, TranslationOptions
#-
from . import models

@register(models.MyFile)
class MyFileTranslationOptions(TranslationOptions):
    fields = ('description', 'alt_text')
