from django.urls import path
#-
from . import views
from . import views_admin

app_name = 'blog_posting'

urlpatterns = [
    path('add', views_admin.Create.as_view(), name='Create'),
    path('<int:pk>/edit', views_admin.Edit.as_view(), name='Update'),
    path('<int:pk>/delete', views_admin.Destroy.as_view(), name='Destroy'),
    path('<int:pk>/publish', views_admin.Publish.as_view(), name='Publish'),
    path('<int:pk>/unpublish', views_admin.Unpublish.as_view(),
        name='Unpublish'),

    path('<int:pk>.<str:format>', views_admin.Display.as_view(),
        name='Display'),
    path('<int:pk>/image-<str:style>', views.serve_files, name='Image'),
    path('<int:pk>/image', views.serve_files, name='Image'),

    path('', views_admin.List.as_view(), name='Index'),
]
