from modeltranslation.translator import register, TranslationOptions
#-
from . import models

@register(models.Event)
class EventTranslationOptions(TranslationOptions):
    fields = ('title', 'body', 'summary', 'slug')
