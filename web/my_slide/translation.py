from modeltranslation.translator import register, TranslationOptions
#-
from . import models

@register(models.MySlide)
class MySlideTranslationOptions(TranslationOptions):
    fields = ('description',)
