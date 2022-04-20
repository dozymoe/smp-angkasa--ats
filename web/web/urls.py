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
from django.urls import include, path, re_path
from django.utils.translation import gettext_lazy as _
#-
from website import views

urlpatterns = [
    re_path(r'^i18n/', include('django.conf.urls.i18n')),

    path('news/', include('blog_posting.urls', namespace='BlogPosting')),
]

urlpatterns += i18n_patterns(
    path(_('news/'), include('blog_posting.urls_lang',
        namespace='BlogPostingLang')),
    path(_('events/'), include('my_event.urls_lang', namespace='EventLang')),
    path(_('files/'), include('my_files.urls', namespace='MyFile')),
    path('admin/editor-helptext.<str:format>', views.EditorHelpText.as_view(),
        name='EditorHelpText'),
    path('index.<str:format>', views.Home.as_view(), name='HomeLang'),
    path('', include('web_page.urls_lang', namespace='WebPageLang')),

    prefix_default_language=True,
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [
    path('', views.home, name='Home'),
]
