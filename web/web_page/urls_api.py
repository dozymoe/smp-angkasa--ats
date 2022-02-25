from django.urls import path
#-
from . import views_api

app_name = 'web_page'

urlpatterns = [
    path('', views_api.List.as_view(), name='Index'),
]
