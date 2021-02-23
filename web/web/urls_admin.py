"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from copy import copy
from django.contrib import admin
from django.urls import path
#-
from website import views
from .urls_common import urlpatterns as base_urlpatterns

urlpatterns = copy(base_urlpatterns)

urlpatterns += [
    path('admin/', admin.site.urls),
    path('index.<str:format>', views.Home.as_view(), name='Home'),

    path('', views.Home.as_view()),
]