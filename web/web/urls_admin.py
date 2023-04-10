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
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.utils.translation import gettext_lazy as _
#-
from website import views, views_admin

urlpatterns = [
    path('admin/editor-helptext.<str:format>', views.EditorHelpText.as_view(),
            name='EditorHelpText'),
    path('account/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    path('api/render-html', views_admin.ReSTPreview.as_view()),
    path('api/files/', include('my_files.urls_api', namespace='MyFileApi')),
    path('api/web_pages/', include('web_page.urls_api',
            namespace='WebPageApi')),

    path('blog-posts/', include('blog_posting.urls_admin',
            namespace='BlogPosting')),
    path('events/', include('my_event.urls_admin', namespace='Event')),
    path('web-pages/', include('web_page.urls_admin', namespace='WebPage')),
    path('files/', include('my_files.urls_admin',
            namespace='MyFile')),
    path('slides/', include('my_slide.urls_admin', namespace='MySlide')),
    path('front-contents/', include('my_front_content.urls_admin',
            namespace='FrontContent')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    path(_('news/'), include('blog_posting.urls_lang',
        namespace='BlogPostingLang')),
    path(_('events/'), include('my_event.urls_lang', namespace='EventLang')),
    path('index.<str:format>', views.Home.as_view(), name='HomeLang'),
    path('', include('web_page.urls_lang', namespace='WebPageLang')),

    prefix_default_language=True,
)

urlpatterns += [
    path('dashboard/', views_admin.Home.as_view()),
    path('', views_admin.Home.as_view(), name='Home'),
]
