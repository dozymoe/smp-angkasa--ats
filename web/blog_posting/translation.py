from modeltranslation.translator import register, TranslationOptions
#-
from . import models

@register(models.BlogPosting)
class BlogPostingTranslationOptions(TranslationOptions):
    fields = ('title', 'body', 'summary', 'slug')
