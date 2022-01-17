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
from my_files.views import serve_files
from website import views, views_admin

urlpatterns = [
    path('account/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    path('api/render-html', views_admin.ReSTPreview.as_view()),
    path('uploads/<path:path>', serve_files),
]

urlpatterns += i18n_patterns(
    path('blog-posts/', include('blog_posting.urls_admin',
            namespace='BlogPosting')),
    path('web-pages/', include('web_page.urls_admin', namespace='WebPage')),
    path('files/', include('my_files.urls_admin',
            namespace='MyFile')),
    path('admin/editor-helptext.<str:format>', views.EditorHelpText.as_view(),
        name='EditorHelpText'),

    prefix_default_language=False,
)

# Quickfixes
urlpatterns += [
    path('ppdb.<str:format>', RedirectView.as_view(url='/'), name='Ppdb'),
]

urlpatterns += [
    path('dashboard/', views_admin.Home.as_view()),
    path('', views_admin.Home.as_view(), name='Home'),
]
