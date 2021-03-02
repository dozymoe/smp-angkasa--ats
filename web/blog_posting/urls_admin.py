from django.urls import path
#-
from . import views_admin

app_name = 'blog_posting'

urlpatterns = [
    path('add', views_admin.Create.as_view(), name='Create'),
    path('<int:pk>/edit', views_admin.Create.as_view(), name='Update'),
    path('<int:pk>/delete', views_admin.Create.as_view(), name='Destroy'),
    path('<str:slug>-<int:pk>', views_admin.Display.as_view(), name='Display'),
    path('', views_admin.List.as_view(), name='Index'),
]
