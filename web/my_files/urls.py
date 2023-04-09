"""Django routes for working with files
"""
from django.urls import path
#-
from . import views

app_name = 'my_files'

urlpatterns = [
    path('<int:pk>/view-<str:style>', views.serve_files, name='Display'),
    path('<int:pk>/view', views.serve_files, name='Display'),
]
