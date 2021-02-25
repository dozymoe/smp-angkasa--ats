from django.urls import path
#-
from . import views_admin

app_name = 'blog_posting'

urlpatterns = [
    path('add', views_admin.Create.as_view(), name='Create'),
    path('<int:pk>/edit', views_admin.Create.as_view(), name='Update'),
]
