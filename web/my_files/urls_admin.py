"""Django routes for managing files
"""
from django.urls import path
#-
from . import urls
from . import views_admin

app_name = 'my_files'

urlpatterns = [
    path('add', views_admin.Create.as_view(), name='Create'),
    path('<int:pk>/edit', views_admin.Edit.as_view(), name='Update'),
    path('<int:pk>/delete', views_admin.Destroy.as_view(), name='Destroy'),

    *urls.urlpatterns,
    path('', views_admin.List.as_view(), name='Index'),
]
