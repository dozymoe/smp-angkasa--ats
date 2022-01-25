from django.urls import path
#-
from . import views

app_name = 'blog_posting'

urlpatterns = [
    path('<str:slug>.<str:format>', views.Display.as_view(),
        name='Display'),
    path('<str:slug>/image-<str:style>', views.serve_files, name='Image'),
    path('<str:slug>/image', views.serve_files, name='Image'),
]
