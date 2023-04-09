"""Django routes for working with files
"""
from django.urls import path
#-
from . import views_api

app_name = 'my_files'

urlpatterns = [
    path('', views_api.List.as_view(), name='Index'),
]
