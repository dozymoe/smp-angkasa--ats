from django.urls import path
#-
from . import views

app_name = 'blog_posting'

urlpatterns = [
    path('<str:slug>.<str:format>', views.Display.as_view(),
        name='Display'),
]
