"""Django routes for managing slideshows
"""
from django.urls import path
#-
from . import views_admin

app_name = 'my_slide'

urlpatterns = [
    path('add', views_admin.Create.as_view(), name='Create'),
    path('<int:pk>/edit', views_admin.Edit.as_view(), name='Update'),
    path('<int:pk>/delete', views_admin.Destroy.as_view(), name='Destroy'),
    path('<int:pk>/move/first', views_admin.move_first, name='MoveFirst'),
    path('<int:pk>/move/up', views_admin.move_up, name='MoveUp'),
    path('<int:pk>/move/down', views_admin.move_down, name='MoveDown'),
    path('<int:pk>/move/last', views_admin.move_last, name='MoveLast'),

    path('', views_admin.List.as_view(), name='Index'),
]
