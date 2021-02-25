from django.contrib import admin
#-
from . import models

admin.site.register(models.ThingKeyword)
admin.site.register(models.ThingKeywordField)
