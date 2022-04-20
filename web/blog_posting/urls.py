from django.urls import path
#-
from . import views

app_name = 'blog_posting'

urlpatterns = [
    path('<int:pk>/image-<str:style>', views.serve_files, name='Image'),
    path('<int:pk>/image', views.serve_files, name='Image'),
]
