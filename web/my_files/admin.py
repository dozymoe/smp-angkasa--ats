from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
#-
from . import models

class MyFilesAdmin(TabbedTranslationAdmin):
    save_on_top = True


admin.site.register(models.MyFile, MyFilesAdmin)
