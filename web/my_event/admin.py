"""Django contrib admin configuration
"""
from django.contrib import admin
#-
from . import models

admin.site.register(models.Event)
