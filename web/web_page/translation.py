from modeltranslation.translator import register, TranslationOptions
#-
from . import models

@register(models.WebPage)
class WebPageTranslationOptions(TranslationOptions):
    fields = ('title', 'body', 'summary', 'slug')
