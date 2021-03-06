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
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
#-
from website import views_admin

urlpatterns = [
    path('account/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    path('api/render-html', views_admin.ReSTPreview.as_view()),
]

urlpatterns += i18n_patterns(
    path('blog-posts/', include('blog_posting.urls_admin',
            namespace='BlogPosting')),

    prefix_default_language=False,
)

# Quickfixes
urlpatterns += [
    path('ppdb.<str:format>', RedirectView.as_view(url='/'), name='Ppdb'),
]

urlpatterns += [
    path('', views_admin.Home.as_view(), name='Home'),
]
