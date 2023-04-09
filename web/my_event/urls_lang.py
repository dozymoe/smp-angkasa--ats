"""Django routes for multilingual events
"""
from django.urls import path
#-
from . import views

app_name = 'my_event'

urlpatterns = [
    path('<str:slug>.<str:format>', views.Display.as_view(),
        name='Display'),
]
