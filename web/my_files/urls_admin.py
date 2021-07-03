from django.urls import path
#-
from . import views_admin

app_name = 'my_files'

urlpatterns = [
    path('add', views_admin.Create.as_view(), name='Create'),
    path('<int:pk>/delete', views_admin.Destroy.as_view(), name='Destroy'),

    path('', views_admin.List.as_view(), name='Index'),
]
