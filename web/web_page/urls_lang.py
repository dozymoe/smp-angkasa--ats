"""Django routes for multilingual pages
"""
from django.urls import path
#-
from . import views

app_name = 'web_page'

urlpatterns = [
    path('<str:slug>.<str:format>', views.Display.as_view(),
        name='Display'),
]
